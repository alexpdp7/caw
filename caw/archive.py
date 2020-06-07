import json


class Archive:
    def __init__(self, path):
        self.path = path

    def _get_tweets(self):
        with open(self.path / "data" / "tweet.js") as f:
            content = f.read()
        return json.loads(content[25:])


if __name__ == "__main__":
    import pathlib
    import sys

    print(Archive(pathlib.Path(sys.argv[1]))._get_tweets())
