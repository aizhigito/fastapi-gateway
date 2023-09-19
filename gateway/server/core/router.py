import importlib

import cachetools
from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import selectinload

from server.core.database import SessionLocal
from server.core.database.models import Scope
from server.core.database.crud import CRUD
from server.core.decorators import to_microservice
from server.utils.router import make_route, get_params_from_path, cache


class ApiGateway(APIRouter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_routes_from_db()

    def add_routes_from_db(self):
        scope_crud = CRUD(Scope)
        with SessionLocal() as db:
            scopes = scope_crud.get_multi(db, options=[selectinload(Scope.microservice)])
            for scope in scopes:
                if scope.is_active:
                    params = get_params_from_path(scope.path)
                    func_name = scope.name.replace(' ', '_').lower()
                    decorated_func = to_microservice(make_route(func_name, scope, params), scope)
                    response_model = None
                    if scope.response_model:
                        module_name, class_name = scope.response_model.rsplit(".", 1)
                        module = importlib.import_module(module_name)
                        response_model = getattr(module, class_name)

                    self.add_api_route(
                        scope.path,
                        decorated_func,
                        response_model=response_model,
                        methods=[scope.method],
                        tags=[f"Microservice: {scope.microservice.name if scope.microservice else 'Without microservice'}"],
                    )


class GatewayRouter(FastAPI):
    _route_len: int = 0

    async def __call__(self, scope, receive, send):
        if not self._route_len or cache.get("need_reload", False):
            api_router = ApiGateway()
            if self._route_len:
                for route in self.routes[-self._route_len:]:
                    self.routes.remove(route)
            self.include_router(api_router)
            self._route_len = len(api_router.routes)
            cache["need_reload"] = False
        await super().__call__(scope, receive, send)

    @cachetools.cached(cache, key=lambda *args: "openapi_cache")
    def openapi(self):
        self.openapi_schema = None
        return super().openapi()
