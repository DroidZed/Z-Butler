from bot import ZBot
from utils import Env


def main() -> None:
    bot: ZBot = ZBot()

    bot.run(Env.TOKEN)


if __name__ == "__main__":
    main()
