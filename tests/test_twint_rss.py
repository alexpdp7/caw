from starlette import testclient

from caw import twint_rss


# This test seems to fail on py38?
def test():
    client = testclient.TestClient(twint_rss.app)
    # this account tweets a daily horoscope
    response = client.get("/tweets/horroroscope")
    assert "Dear Taurus" in response.text
