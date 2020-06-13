import dataclasses
import enum
from typing import List, Any, Dict, Tuple

from caw.archive.int_range import IntRange, make_int_range


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
    sizes: Dict[str, Size]
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
    variants: List[Variant]
    aspect_ratio: AspectRatio


@dataclasses.dataclass
class Video(Medium):
    variants: List[Variant]
    aspect_ratio: AspectRatio
    duration_millis: int
    monetizable: bool


def make_media(media: List[Any]) -> List[Medium]:
    return [_make_medium(medium) for medium in media]


def _make_medium(medium_json: Any) -> Medium:
    display_url = medium_json.pop("display_url")
    assert isinstance(display_url, str)

    expanded_url = medium_json.pop("expanded_url")
    assert isinstance(expanded_url, str)

    id = int(medium_json.pop("id"))
    id_str = medium_json.pop("id_str")
    assert str(id) == id_str

    indices = make_int_range(medium_json.pop("indices"))

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


def _make_sizes(sizes: Dict[str, Any]) -> Dict[str, Size]:
    return dict(
        [_make_size(size, content_json) for size, content_json in sizes.items()]
    )


def _make_size(size: str, content_json: Any) -> Tuple[str, Size]:
    height = int(content_json.pop("h"))
    width = int(content_json.pop("w"))

    resize = Resize[content_json.pop("resize").upper()]

    assert not content_json
    return size, Size(height=height, width=width, resize=resize)


def _make_aspect_ratio(aspect_ratio: List[str]) -> AspectRatio:
    return AspectRatio(int(aspect_ratio[0]), int(aspect_ratio[1]))


def _make_variants(variants_json: Any) -> List[Variant]:
    return [_make_variant(variant_json) for variant_json in variants_json]


def _make_variant(variant_json: Any) -> Variant:
    bitrate = variant_json.pop("bitrate", None)
    if bitrate:
        bitrate = int(bitrate)

    content_type = variant_json.pop("content_type")
    assert isinstance(content_type, str)

    url = variant_json.pop("url")
    assert isinstance(url, str)

    assert not variant_json, variant_json

    return Variant(url=url, bitrate=bitrate, content_type=content_type)
