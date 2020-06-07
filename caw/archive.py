import dataclasses
import datetime
import enum
import json


class Archive:
    def __init__(self, path):
        self.path = path

    def _get_tweets(self):
        with open(self.path / "data" / "tweet.js") as f:
            content = f.read()
        return json.loads(content[25:])

    def get_tweets(self):
        return [_make_tweet(t) for t in self._get_tweets()]


@dataclasses.dataclass
class IntRange:
    begin: int
    end: int


Resize = enum.Enum("Resize", "FIT THUMB CROP")


@dataclasses.dataclass
class Size:
    width: int
    height: int
    resize: Resize


@dataclasses.dataclass
class Medium:
    display_url: str
    expanded_url: str
    id: int
    indices: IntRange
    media_url_https: str
    sizes: [Size]
    source_status_id: int
    source_user_id: int
    url: str


@dataclasses.dataclass
class Photo(Medium):
    pass


@dataclasses.dataclass
class Variant:
    url: str
    bitrate: int
    content_type: str


@dataclasses.dataclass
class AspectRatio:
    width: int
    height: int


@dataclasses.dataclass
class AnimatedGif(Medium):
    variants: [Variant]
    aspect_ratio: AspectRatio


@dataclasses.dataclass
class Video(Medium):
    variants: [Variant]
    aspect_ratio: AspectRatio
    duration_millis: int
    monetizable: bool


@dataclasses.dataclass
class Url:
    display_url: str
    expanded_url: str
    indices: IntRange
    url: str


@dataclasses.dataclass
class UserMention:
    name: str
    screen_name: str
    indices: IntRange
    id: int


@dataclasses.dataclass
class Hashtag:
    text: str
    indices: IntRange


@dataclasses.dataclass
class Symbol:
    indices: IntRange
    text: str


@dataclasses.dataclass
class Entities:
    hashtags: [Hashtag]
    user_mentions: [UserMention]
    urls: [Url]
    media: [Medium]
    symbols: [Symbol]


@dataclasses.dataclass
class Tweet:
    retweeted: bool
    source: str
    lang: str
    full_text: str
    favorited: bool
    possibly_sensitive: bool
    id: int
    retweet_count: int
    truncated: bool
    favorite_count: int
    display_text_range: IntRange
    created_at: datetime.datetime
    in_reply_to_status_id: int
    in_reply_to_user_id: int
    in_reply_to_screen_name: str
    entities: Entities
    extended_entities: Entities


def _date_from_str(s):
    """
    >>> _date_from_str('Sat Jun 06 12:09:03 +0000 2020')
    datetime.datetime(2020, 6, 6, 12, 9, 3, tzinfo=datetime.timezone.utc)
    """
    return datetime.datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")


def _make_tweet(json_tweet):
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

    created_at = _date_from_str(json_tweet.pop("created_at"))

    truncated = json_tweet.pop("truncated")
    assert isinstance(truncated, bool)

    favorite_count = int(json_tweet.pop("favorite_count"))

    display_text_range_json = json_tweet.pop("display_text_range")
    display_text_range = _make_int_range(display_text_range_json)

    entities = _make_entities(json_tweet.pop("entities"))

    extended_entities_json = json_tweet.pop("extended_entities", None)
    extended_entities = (
        _make_entities(extended_entities_json) if extended_entities_json else None
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


def _make_int_range(int_range_json):
    assert len(int_range_json) == 2
    int_range_json_begin = int(int_range_json[0])
    int_range_json_end = int(int_range_json[1])
    assert int_range_json_end >= int_range_json_begin
    return IntRange(begin=int_range_json_begin, end=int_range_json_end)


def _make_entities(entities_json):
    hashtags = _make_hashtags(entities_json.pop("hashtags", []))
    symbols = _make_symbols(entities_json.pop("symbols", []))
    user_mentions = _make_user_mentions(entities_json.pop("user_mentions", []))
    urls = _make_urls(entities_json.pop("urls", []))
    media = _make_media(entities_json.pop("media", []))

    assert not entities_json, entities_json

    return Entities(
        hashtags=hashtags,
        user_mentions=user_mentions,
        urls=urls,
        media=media,
        symbols=symbols,
    )


def _make_symbols(symbols):
    return [_make_symbol(symbol) for symbol in symbols]


def _make_symbol(symbol_json):
    text = symbol_json.pop("text")
    assert isinstance(text, str)

    indices = _make_int_range(symbol_json.pop("indices"))

    assert not symbol_json
    return Symbol(indices=indices, text=text)


def _make_urls(urls):
    return [_make_url(url) for url in urls]


def _make_url(url_json):
    display_url = url_json.pop("display_url")
    assert isinstance(display_url, str)

    expanded_url = url_json.pop("expanded_url")
    assert isinstance(expanded_url, str)

    indices = _make_int_range(url_json.pop("indices"))

    url = url_json.pop("url")
    assert isinstance(url, str)

    assert not url_json
    return Url(
        display_url=display_url, expanded_url=expanded_url, indices=indices, url=url
    )


def _make_sizes(sizes):
    return dict(
        [_make_size(size, content_json) for size, content_json in sizes.items()]
    )


def _make_size(size, content_json):
    height = int(content_json.pop("h"))
    width = int(content_json.pop("w"))

    resize = Resize[content_json.pop("resize").upper()]

    assert not content_json
    return size, Size(height=height, width=width, resize=resize)


def _make_media(media):
    return [_make_medium(medium) for medium in media]


def _make_medium(medium_json):
    display_url = medium_json.pop("display_url")
    assert isinstance(display_url, str)

    expanded_url = medium_json.pop("expanded_url")
    assert isinstance(expanded_url, str)

    id = int(medium_json.pop("id"))
    id_str = medium_json.pop("id_str")
    assert str(id) == id_str

    indices = _make_int_range(medium_json.pop("indices"))

    media_url = medium_json.pop("media_url")
    media_url_https = medium_json.pop("media_url_https")
    assert media_url[len("http://") :] == media_url_https[len("https://") :]

    sizes = _make_sizes(medium_json.pop("sizes"))

    source_status_id = medium_json.pop("source_status_id", None)
    source_status_id_str = medium_json.pop("source_status_id_str", None)
    if source_status_id:
        source_status_id = int(source_status_id)
        assert str(source_status_id) == source_status_id_str

    source_user_id = medium_json.pop("source_user_id", None)
    source_user_id_str = medium_json.pop("source_user_id_str", None)
    if source_user_id:
        source_user_id = int(source_user_id)
        assert str(source_user_id) == source_user_id_str

    url = medium_json.pop("url")
    assert isinstance(url, str)

    type = medium_json.pop("type")

    if type == "photo":
        assert not medium_json
        return Photo(
            display_url=display_url,
            expanded_url=expanded_url,
            id=id,
            indices=indices,
            media_url_https=media_url_https,
            sizes=sizes,
            source_status_id=source_status_id,
            source_user_id=source_user_id,
            url=url,
        )

    if type == "animated_gif":
        video_info = medium_json.pop("video_info")

        aspect_ratio = _make_aspect_ratio(video_info.pop("aspect_ratio"))

        variants = _make_variants(video_info.pop("variants"))

        assert not video_info, video_info

        assert not medium_json
        return AnimatedGif(
            display_url=display_url,
            expanded_url=expanded_url,
            id=id,
            indices=indices,
            media_url_https=media_url_https,
            sizes=sizes,
            source_status_id=source_status_id,
            source_user_id=source_user_id,
            url=url,
            variants=variants,
            aspect_ratio=aspect_ratio,
        )

    if type == "video":
        video_info = medium_json.pop("video_info")

        aspect_ratio = _make_aspect_ratio(video_info.pop("aspect_ratio"))

        variants = _make_variants(video_info.pop("variants"))

        duration_millis = int(video_info.pop("duration_millis"))

        assert not video_info, video_info

        additional_media_info = medium_json.pop("additional_media_info")

        monetizable = bool(additional_media_info.pop("monetizable"))

        assert additional_media_info.pop("title", "") == ""
        assert additional_media_info.pop("description", "") == ""
        assert additional_media_info.pop("embeddable", True)

        assert not additional_media_info, additional_media_info

        assert not medium_json, medium_json

        return Video(
            display_url=display_url,
            expanded_url=expanded_url,
            id=id,
            indices=indices,
            media_url_https=media_url_https,
            sizes=sizes,
            source_status_id=source_status_id,
            source_user_id=source_user_id,
            url=url,
            variants=variants,
            aspect_ratio=aspect_ratio,
            duration_millis=duration_millis,
            monetizable=monetizable,
        )

    assert False, type


def _make_aspect_ratio(aspect_ratio):
    return AspectRatio(int(aspect_ratio[0]), int(aspect_ratio[1]))


def _make_variants(variants_json):
    return [_make_variant(variant_json) for variant_json in variants_json]


def _make_variant(variant_json):
    bitrate = variant_json.pop("bitrate", None)
    if bitrate:
        bitrate = int(bitrate)

    content_type = variant_json.pop("content_type")
    assert isinstance(content_type, str)

    url = variant_json.pop("url")
    assert isinstance(url, str)

    assert not variant_json, variant_json

    return Variant(url=url, bitrate=bitrate, content_type=content_type)


def _make_user_mentions(user_mentions_json):
    return [
        _make_user_mention(user_mention_json)
        for user_mention_json in user_mentions_json
    ]


def _make_user_mention(user_mention_json):
    name = user_mention_json.pop("name")
    assert isinstance(name, str)

    screen_name = user_mention_json.pop("screen_name")
    assert isinstance(screen_name, str)

    indices = _make_int_range(user_mention_json.pop("indices"))

    id = int(user_mention_json.pop("id"))
    id_str = user_mention_json.pop("id_str")
    assert str(id) == id_str

    assert not user_mention_json.keys(), user_mention_json

    return UserMention(name=name, screen_name=screen_name, indices=indices, id=id)


def _make_hashtags(hashtags_json):
    return [_make_hashtag(hashtag_json) for hashtag_json in hashtags_json]


def _make_hashtag(hashtag_json):
    text = hashtag_json.pop("text")
    assert isinstance(text, str)

    indices = _make_int_range(hashtag_json.pop("indices"))

    assert not hashtag_json, hashtag_json

    return Hashtag(text=text, indices=indices)


if __name__ == "__main__":
    import pathlib
    import sys

    print(Archive(pathlib.Path(sys.argv[1]))._get_tweets())
