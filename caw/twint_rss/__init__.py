import datetime
from typing import Iterable

from starlette.applications import Starlette
from starlette.requests import Request
from starlette_feedgen import FeedEndpoint  # type: ignore

import twint  # type: ignore

from caw.twint import get_timeline

app = Starlette()


class FeedObject:
    def __init__(self, username: str):
        self.username = username


class FeedItem:
    def __init__(self, tweet: twint.tweet.tweet):
        self.tweet = tweet

    @property
    def title(self) -> str:
        return str(self.tweet.tweet)

    @property
    def description(self) -> str:
        return str(self.tweet.tweet)

    @property
    def link(self) -> str:
        return (
            f"https://mobile.twitter.com/{self.tweet.username}/status/{self.tweet.id}"
        )


@app.route("/tweets/{username}")
class Feed(FeedEndpoint):  # type: ignore
    async def get_object(self, request: Request) -> FeedObject:
        return FeedObject(request.path_params["username"])

    def title(self, obj: FeedObject) -> str:
        return f"RSS feed for {obj.username}"

    def description(self, obj: FeedObject) -> str:
        return f"RSS feed for {obj.username}"

    def link(self, obj: FeedObject) -> str:
        return f"https://twitter.com/{obj.username}"

    def get_items(self) -> Iterable[FeedItem]:
        username = self.scope["path_params"]["username"]
        tweets = get_timeline(
            username, datetime.datetime.now() - datetime.timedelta(days=1)
        )
        return map(FeedItem, tweets)
