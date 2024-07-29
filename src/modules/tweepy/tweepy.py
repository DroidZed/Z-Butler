def get_url(tweet_id: str, token: str) -> str:
    return f"https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}&lang=en&token={token}"
