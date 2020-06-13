import json
import pathlib
from typing import List, Any


from caw.archive import tweet


class Archive:
    def __init__(self, path: pathlib.Path):
        self.path = path

    def _get_tweets(self) -> Any:
        with open(self.path / "data" / "tweet.js") as f:
            content = f.read()
        return json.loads(content[25:])

    def get_tweets(self) -> List[tweet.Tweet]:
        return [tweet.make_tweet(t) for t in self._get_tweets()]
