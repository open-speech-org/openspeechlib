"""
Utility functions for HTTP

This will be used as proxy in case we don't want to rely on requests in the future
"""
from urllib import parse
import requests

get = requests.get

HTTPError = requests.exceptions.HTTPError


def extract_query_param_from_url_string(url, param):
    """
    This function extract a query parameter from a URL

```python
from openspeechlib.utils import http
url = "https://librivox.org/api/feed/audiobooks?format=json&limit=50&offset=14450"
offset = http.extract_query_param_from_url_string(url, "offset")
assert offset[0] == "14450"
```

    :param url: A URL String
    :param param:
    :return:
    """
    parsed_url = parse.urlparse(url)
    return parse.parse_qs(parsed_url.query).get(param)
