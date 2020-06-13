import dataclasses
import datetime
from typing import Any, Optional

from caw.archive.dates import date_from_str
from caw.archive.entities import Entities, make_entities
from caw.archive.int_range import IntRange, make_int_range


@dataclasses.dataclass
class Tweet:
    retweeted: bool
    source: str
    lang: str
    full_text: str
    favorited: bool
    possibly_sensitive: Optional[bool]
    id: int
    retweet_count: int
    truncated: bool
    favorite_count: int
    display_text_range: IntRange
    created_at: datetime.datetime
    in_reply_to_status_id: int
    in_reply_to_user_id: int
    in_reply_to_screen_name: Optional[str]
    entities: Entities
    extended_entities: Optional[Entities]


def make_tweet(json_tweet: Any) -> Tweet:
    assert list(json_tweet.keys()) == ["tweet"]
    json_tweet = json_tweet["tweet"]

    retweeted = json_tweet.pop("retweeted")
    assert isinstance(retweeted, bool)

    source = json_tweet.pop("source")
    assert isinstance(source, str)

    lang = json_tweet.pop("lang")
    assert isinstance(lang, str)
    assert len(lang) == 2 or lang == "und"

    full_text = json_tweet.pop("full_text")
    assert isinstance(full_text, str)

    favorited = json_tweet.pop("favorited")
    assert isinstance(favorited, bool)

    possibly_sensitive = json_tweet.pop("possibly_sensitive", None)
    assert possibly_sensitive is None or isinstance(possibly_sensitive, bool)

    id = int(json_tweet.pop("id"))
    id_str = json_tweet.pop("id_str")
    assert str(id) == id_str

    retweet_count = int(json_tweet.pop("retweet_count"))

    created_at = date_from_str(json_tweet.pop("created_at"))

    truncated = json_tweet.pop("truncated")
    assert isinstance(truncated, bool)

    favorite_count = int(json_tweet.pop("favorite_count"))

    display_text_range_json = json_tweet.pop("display_text_range")
    display_text_range = make_int_range(display_text_range_json)

    entities = make_entities(json_tweet.pop("entities"))

    extended_entities_json = json_tweet.pop("extended_entities", None)
    extended_entities = (
        make_entities(extended_entities_json) if extended_entities_json else None
    )

    in_reply_to_status_id = json_tweet.pop("in_reply_to_status_id", None)
    in_reply_to_status_id_str = json_tweet.pop("in_reply_to_status_id_str", None)
    if in_reply_to_status_id:
        in_reply_to_status_id = int(in_reply_to_status_id)
        assert str(in_reply_to_status_id) == in_reply_to_status_id_str
    else:
        assert in_reply_to_status_id_str is None

    in_reply_to_user_id = json_tweet.pop("in_reply_to_user_id", None)
    in_reply_to_user_id_str = json_tweet.pop("in_reply_to_user_id_str", None)
    if in_reply_to_user_id:
        in_reply_to_user_id = int(in_reply_to_user_id)
        assert str(in_reply_to_user_id) == in_reply_to_user_id_str
    else:
        assert in_reply_to_user_id_str is None

    in_reply_to_screen_name = json_tweet.pop("in_reply_to_screen_name", None)
    assert in_reply_to_screen_name is None or isinstance(in_reply_to_screen_name, str)

    assert not json_tweet.keys(), json_tweet

    return Tweet(
        retweeted=retweeted,
        source=source,
        lang=lang,
        full_text=full_text,
        favorited=favorited,
        created_at=created_at,
        possibly_sensitive=possibly_sensitive,
        id=id,
        retweet_count=retweet_count,
        truncated=truncated,
        favorite_count=favorite_count,
        display_text_range=display_text_range,
        in_reply_to_status_id=in_reply_to_status_id,
        in_reply_to_user_id=in_reply_to_user_id,
        in_reply_to_screen_name=in_reply_to_screen_name,
        entities=entities,
        extended_entities=extended_entities,
    )
