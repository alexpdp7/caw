import dataclasses
from typing import List


@dataclasses.dataclass
class IntRange:
    begin: int
    end: int


def make_int_range(int_range_json: List[str]) -> IntRange:
    assert len(int_range_json) == 2
    int_range_json_begin = int(int_range_json[0])
    int_range_json_end = int(int_range_json[1])
    assert int_range_json_end >= int_range_json_begin
    return IntRange(begin=int_range_json_begin, end=int_range_json_end)
