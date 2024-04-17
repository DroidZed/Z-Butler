from litestar import Router

from ..controllers import MainController


mainController: Router = Router(path="/v1", route_handlers=[MainController])
