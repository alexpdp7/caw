import dataclasses
from typing import List, Any

from caw.archive.int_range import IntRange, make_int_range
from caw.archive.media import Medium, make_media


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
    hashtags: List[Hashtag]
    user_mentions: List[UserMention]
    urls: List[Url]
    media: List[Medium]
    symbols: List[Symbol]


def make_entities(entities_json: Any) -> Entities:
    hashtags = _make_hashtags(entities_json.pop("hashtags", []))
    symbols = _make_symbols(entities_json.pop("symbols", []))
    user_mentions = _make_user_mentions(entities_json.pop("user_mentions", []))
    urls = _make_urls(entities_json.pop("urls", []))
    media = make_media(entities_json.pop("media", []))

    assert not entities_json, entities_json

    return Entities(
        hashtags=hashtags,
        user_mentions=user_mentions,
        urls=urls,
        media=media,
        symbols=symbols,
    )


def _make_symbols(symbols: List[Any]) -> List[Symbol]:
    return [_make_symbol(symbol) for symbol in symbols]


def _make_symbol(symbol_json: Any) -> Symbol:
    text = symbol_json.pop("text")
    assert isinstance(text, str)

    indices = make_int_range(symbol_json.pop("indices"))

    assert not symbol_json
    return Symbol(indices=indices, text=text)


def _make_urls(urls: Any) -> List[Url]:
    return [_make_url(url) for url in urls]


def _make_url(url_json: Any) -> Url:
    display_url = url_json.pop("display_url")
    assert isinstance(display_url, str)

    expanded_url = url_json.pop("expanded_url")
    assert isinstance(expanded_url, str)

    indices = make_int_range(url_json.pop("indices"))

    url = url_json.pop("url")
    assert isinstance(url, str)

    assert not url_json
    return Url(
        display_url=display_url, expanded_url=expanded_url, indices=indices, url=url
    )


def _make_user_mentions(user_mentions_json: Any) -> List[UserMention]:
    return [
        _make_user_mention(user_mention_json)
        for user_mention_json in user_mentions_json
    ]


def _make_user_mention(user_mention_json: Any) -> UserMention:
    name = user_mention_json.pop("name")
    assert isinstance(name, str)

    screen_name = user_mention_json.pop("screen_name")
    assert isinstance(screen_name, str)

    indices = make_int_range(user_mention_json.pop("indices"))

    id = int(user_mention_json.pop("id"))
    id_str = user_mention_json.pop("id_str")
    assert str(id) == id_str

    assert not user_mention_json.keys(), user_mention_json

    return UserMention(name=name, screen_name=screen_name, indices=indices, id=id)


def _make_hashtags(hashtags_json: Any) -> List[Hashtag]:
    return [_make_hashtag(hashtag_json) for hashtag_json in hashtags_json]


def _make_hashtag(hashtag_json: Any) -> Hashtag:
    text = hashtag_json.pop("text")
    assert isinstance(text, str)

    indices = make_int_range(hashtag_json.pop("indices"))

    assert not hashtag_json, hashtag_json

    return Hashtag(text=text, indices=indices)
