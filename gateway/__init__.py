""" Gateway module. """

__version__ = "0.0.1-beta-14-dev"

from .server.core.router import GatewayRouter as GatewayRouter # noqa
from .server.routes import gateway_router as gateway_crud_router # noqa
