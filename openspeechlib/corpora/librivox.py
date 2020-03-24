"""
Implementation to get LibriVox audios
"""
import logging
import os

from openspeechlib.corpora import base
from openspeechlib.utils import (
    file,
    http
)

LOGGER = logging.getLogger(__name__)


class LibriVox(base.BaseCorpus):
    """
    Download LibriBox Information

    Example

```python
from openspeechlib.corpora.librivox import LibriVox
lv = LibriVox()
content = lv.fetch_all()
```
    """
    _api_url = "https://librivox.org/api/feed/audiobooks?{}"

    corpus_name = "librivox"

    DEFAULT_ARGS = {
        "format": "json",
        "limit": base.PAGE_SIZE,
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

    def fetch(self, _from, _to, **kwargs):
        kwargs["offset"] = _from
        kwargs["limit"] = _to - _from
        url = self.url_builder(**kwargs)
        LOGGER.debug(f"Fetching data from {url}")
        response = http.get(url)
        if response.ok:
            return response.json()["books"]
        response.raise_for_status()

    def fetch_all(self):
        file.create_folder(os.path.join(base.CORPORA_FOLDER, self.corpus_name))
        books = list()
        _from = 0
        _to = base.PAGE_SIZE
        for _ in range(base.MAX_REQUESTS):
            books.extend(self.fetch(_from=_from, _to=_to, fields=LibriVox.SLIM_FIELDS))
            _from = _to
            _to = _to + base.PAGE_SIZE
        return books

    def url_builder(self, **kwargs):
        merged_kwargs = {**self.DEFAULT_ARGS, **kwargs}
        if "fields" in merged_kwargs:
            merged_kwargs["fields"] = "{{{fields}}}".format(fields=",".join(merged_kwargs["fields"]))
        return self._api_url.format(self.kwargs_to_query_params(**merged_kwargs))
