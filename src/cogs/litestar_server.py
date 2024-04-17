import asyncio
from discord.ext.commands import Bot, Cog
from litestar import Litestar
from uvicorn import Config, Server

from www.routes import mainController


class LiteStarServer(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.app = Litestar(route_handlers=[mainController])

    @Cog.listener(name="on_ready")
    async def on_ready(self) -> None:
        loop = asyncio.new_event_loop()
        config = Config(app=self.app, loop="asyncio", port=5000)
        server = Server(config)

        loop.run_until_complete(await server.serve())  # type: ignore


def setup(bot: Bot) -> None:
    bot.add_cog(LiteStarServer(bot))
