from litestar import Controller, get


class MainController(Controller):
    path = "/"

    @get("/")
    async def index(self) -> dict[str, str]:
        return {"message": "Hello, world!"}
