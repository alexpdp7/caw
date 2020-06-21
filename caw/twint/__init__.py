import datetime
import typing

import twint  # type: ignore


def get_timeline(
    username: str, since: datetime.datetime
) -> typing.List[twint.tweet.tweet]:
    c = twint.Config()
    c.Username = username
    c.Since = since.strftime("%Y-%m-%d %H:%M:%S")

    tweets: typing.List[twint.tweet.tweet] = []
    c.Store_object = True
    c.Store_object_tweets_list = tweets
    twint.run.Search(c)
    return tweets
