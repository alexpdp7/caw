import datetime


def date_from_str(s: str) -> datetime.datetime:
    """
    >>> date_from_str('Sat Jun 06 12:09:03 +0000 2020')
    datetime.datetime(2020, 6, 6, 12, 9, 3, tzinfo=datetime.timezone.utc)
    """
    return datetime.datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")
