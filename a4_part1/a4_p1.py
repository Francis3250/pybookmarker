# NAME Wentai Yan
# EMAIL wentaiy@uci.edu

import urllib.request
import urllib.parse
import urllib.error
import json
import bookmark_connection as bmc
from bookmark_connection import BookmarkProtocol

"""
The following code snippets can be used to help you prepare your test function:
The url to use for testing.
Be sure to run bookmark_server.py before making requests!

url = 'http://localhost:8000'

The format to use for your request data.
Don't forget to encode before sending a request!

json = {'data':bmc.BookmarkProtocol.format(
                                BookmarkProtocol(BookmarkProtocol.ADD, data))}
"""

SERVER_URL = "http://localhost:8000"


def _make_payload(url_to_add: str) -> bytes:
    """Build properly-encoded POST body for one bookmark URL."""
    proto_msg = BookmarkProtocol.format(
        BookmarkProtocol(BookmarkProtocol.ADD, url_to_add)
    )
    # The format expected by the server bookmark_server.py is url-encoded form:
    #   data=<proto_msg>
    return urllib.parse.urlencode({"data": proto_msg}).encode()


def http_api_test():
    """Send three (or more) ADD commands to the running bookmark server."""
    test_urls = [
        "https://www.python.org",
        "https://openai.com",
        "https://docs.python.org/3/library/urllib.html",
    ]

    for link in test_urls:
        req = urllib.request.Request(
            SERVER_URL,
            data=_make_payload(link),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                body = resp.read().decode()
                status = resp.status
                print(f"[OK {status}]  {link}  →  {body.strip()}")
        except urllib.error.HTTPError as e:
            print(f"[HTTP {e.code}] {link}  →  {e.reason}")
        except urllib.error.URLError as e:
            print(f"[CONNECTION ERROR] {link}  →  {e.reason}")


if __name__ == '__main__':
    http_api_test()
