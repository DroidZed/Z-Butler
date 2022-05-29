from tweepy import BadRequest, Forbidden
from tweepy.asynchronous import AsyncClient

from classes.singleton_class import SingletonClass
from classes.tweet_model import TweetModel
from config.main import (
    TWITTER_BEARER_TOKEN,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)


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
