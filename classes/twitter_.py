from tweepy import BadRequest, Forbidden
from tweepy.asynchronous import AsyncClient

from classes.singleton_class import SingletonClass
from config.main import (
    TWITTER_BEARER_TOKEN,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)


class TweetModel:
    """
    A simple model class to wrap the data received by querying the Twitter API.
    """

    __slots__ = ["__t_id", "__text", "__err"]

    def __init__(self, t_id: str = "", text: str = "", err=""):
        self.__t_id: int = t_id
        self.__text: str = text
        self.__err: str = err

    @property
    def t_id(self):
        return self.__t_id

    @property
    def text(self):
        return self.__text

    @property
    def err(self):
        return self.__err

    @t_id.setter
    def t_id(self, t_id: str):
        self.__t_id = t_id

    @text.setter
    def text(self, text: str):
        self.__text = text

    @err.setter
    def err(self, err: str):
        self.__err = err

    def __dict__(self):
        return {"id": self.t_id, "text": self.__text}

    def __str__(self):
        return "tweet:{'id': '" + self.t_id + "', 'text': '" + self.text + "'}"

    def __repr__(self):
        return "tweet:{'id': '" + self.t_id + "', 'text': '" + self.text + "'}"


class TweepyWrapper(metaclass=SingletonClass):
    def __init__(self):
        self.client = AsyncClient(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True,
        )

    async def tweet(self, text: str, reply=False, tweet_id=-1) -> TweetModel | dict:

        try:
            tweet = await self.client.create_tweet(
                in_reply_to_tweet_id=tweet_id if reply and tweet_id > 0 else None, text=text, user_auth=True
            )

            return TweetModel(tweet.data["id"], tweet.data["text"])

        except (BadRequest, Forbidden) as e:
            return TweetModel(err=" ".join(_ for _ in e.api_messages))
