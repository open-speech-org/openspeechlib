"""
Implementation to get LibriVox audios
"""
import json
import requests

from openspeechlib.corpora.base import BaseCorpus


class LibriVox(BaseCorpus):
    """
    Download LibriBox Information

    Example

```python
from openspeechlib.corpora.librivox import LibriVox
lv = LibriVox()
content = lv.fetch(fields=LibriVox.SLIM_FIELDS)
```
    """
    _api_url = "https://librivox.org/api/feed/audiobooks?{}"

    DEFAULT_ARGS = {
        "format": "json",
        "limit": 50,
        "offset": 0
    }

    SLIM_FIELDS = [
        "id",
        "title",
        "url_text_source",
        "language",
        "url_zip_file",
        "totaltimesecs",
        "url_librivox"
    ]

    def fetch(self, _from=None, _to=None, **kwargs):
        response = requests.get(self.url_builder(**kwargs))
        if response.ok:
            return response.json()["books"]
        response.raise_for_status()

    def url_builder(self, **kwargs):
        merged_kwargs = {**self.DEFAULT_ARGS, **kwargs}
        if "fields" in merged_kwargs:
            merged_kwargs["fields"] = "{{{fields}}}".format(fields=",".join(merged_kwargs["fields"]))
        return self._api_url.format(self.kwargs_to_query_params(**merged_kwargs))
