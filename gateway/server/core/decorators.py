from functools import wraps
from typing import TYPE_CHECKING

from aiohttp import ContentTypeError, ClientConnectorError
from fastapi import Request, Response, HTTPException, status

from server.core.request import fetch
from server.utils.body import unzip_body_object
from server.utils.form import unzip_form_params
from server.utils.query import unzip_query_params
from server.utils.request import create_request_data
from server.utils.headers import (
    generate_headers_for_microservice, inheritance_service_headers,
)


if TYPE_CHECKING:
    from server.core.database.models import Scope


def to_microservice(func, scope_model: "Scope"):
    @wraps(func)
    async def wrapper(request: Request, response: Response, **kwargs):
        scope = request.scope
        scope_method = scope["method"].lower()
        content_type = str(request.headers.get('Content-Type'))
        request_form = (
            await request.form() if 'x-www-form-urlencoded' in content_type else None
        )

        prepare_microservice_path = f"{scope_model.microservice.base_url}{scope_model.path}"
        if scope_model.microservice_path:
            prepare_microservice_path = f"{scope_model.microservice.base_url}{scope_model.microservice_path}"

        microservice_url = prepare_microservice_path.format(**scope["path_params"])
        request_body = await unzip_body_object(
            necessary_params=scope_model.body_params,
            all_params=kwargs,
        )
        request_query = await unzip_query_params(
            necessary_params=scope_model.query_params, all_params=kwargs
        )
        request_form = await unzip_form_params(
            necessary_params=scope_model.form_params,
            request_form=request_form,
            all_params=kwargs,
        )

        request_headers = generate_headers_for_microservice(
            headers=request.headers,
        )

        request_data = create_request_data(
            form=request_form,
            body=request_body,
        )
        try:
            (
                resp_data,
                status_code_from_service,
                microservice_headers,
            ) = await fetch(
                url=microservice_url,
                method=scope_method,
                data=request_data,
                query_params=request_query,
                headers=request_headers,
            )

        except ClientConnectorError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service is unavailable.",
            )
        except ContentTypeError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Service error.",
            )

        if scope_model.override_headers:
            service_headers = inheritance_service_headers(
                gateway_headers=response.headers,
                service_headers=microservice_headers,
            )
            for key, value in service_headers.items():
                response.headers.append(key, value)
        response.status_code = status_code_from_service
    return wrapper
