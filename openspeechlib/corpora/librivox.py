"""
Implementation to get LibriVox audios
"""
import logging
import os
import json

from openspeechlib.corpora import base
from openspeechlib.utils import (
    file,
    http
)

LOGGER = logging.getLogger(__name__)

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


class LibriVox(base.BaseCorpus):
    """
    Download LibriBox Information

    Example

```python
import logging
logging.basicConfig(level=logging.INFO)
from openspeechlib.corpora.librivox import LibriVox
lv = LibriVox()
content = lv.fetch_all()
lv.export_books_by_language()
```
    """

    _api_url = "https://librivox.org/api/feed/audiobooks?{}"
    _last_successful_url = None
    corpus_name = "librivox"
    _books = list()

    @property
    def corpus_folder(self):
        return os.path.join(
            file.get_home_folder(),
            base.CORPORA_FOLDER,
            self.corpus_name
        )

    @property
    def _last_successful_url_file(self):
        return os.path.join(
            self.corpus_folder,
            base.LAST_FETCHED_URL.format(self.corpus_name)
        )

    @property
    def corpus_data_file(self):
        return os.path.join(
            self.corpus_folder,
            "corpus.json"
        )

    def __init__(self):
        file.create_folder(
            self.corpus_folder
        )

    def fetch(self, _from, _to, **kwargs):
        kwargs["offset"] = _from
        kwargs["limit"] = _to - _from
        url = self.url_builder(**kwargs)
        LOGGER.info(f"Fetching data from {url}")
        response = http.get(url)
        if response.ok:
            self._last_successful_url = url
            books = response.json()["books"]
            LOGGER.debug(books)
            return books
        response.raise_for_status()

    def _get_last_from_and_to_params(self, remember_cache):
        _from = 0
        _to = base.PAGE_SIZE
        if remember_cache:
            last_url = file.get_content_from_file(self._last_successful_url_file)
            offset = http.extract_query_param_from_url_string(last_url, "offset")
            if offset and isinstance(offset, list):
                _from = int(offset[0])
                _to = _from + base.PAGE_SIZE
        return _from, _to

    def fetch_all(self, remember_cache=True):
        self._books = list()

        _from, _to = self._get_last_from_and_to_params(remember_cache)
        try:
            for _ in range(base.MAX_REQUESTS):
                self._books.extend(self.fetch(_from=_from, _to=_to, fields=SLIM_FIELDS))
                _from = _to
                _to = _to + base.PAGE_SIZE
        except http.HTTPError as http_error:
            LOGGER.error(f"HTTP Error on range from: {_from} to: {_to}")
            LOGGER.error(http_error)
            LOGGER.info(f"Interrupting execution in range from: {_from} to: {_to}")
            LOGGER.info("Saving previous results")
        books = self.retrieve_and_merge_previous_content_with_new_books(self._books)
        self.store_results(books)
        return self._books

    def retrieve_and_merge_previous_content_with_new_books(self, books):
        merged_books = books
        previous_content = file.get_content_from_file(self.corpus_data_file)
        if previous_content:
            LOGGER.debug("Content from previous file")
            LOGGER.debug(previous_content)
            try:
                previous_books = json.loads(previous_content)
                if isinstance(previous_books, list):
                    LOGGER.info(f"Total records read {len(previous_books)}")
                    LOGGER.info(f"Total records fetched from Internet {len(books)}")
                    previous_books.extend(books)
                    merged_books = previous_books
                    LOGGER.info(f"Total records in memory {len(merged_books)}")
                else:
                    LOGGER.error("Decoding file isn't an array, skipping")
            except json.JSONDecodeError:
                LOGGER.error("Problem loading previous content, skipping")
        return merged_books

    def store_results(self, books):
        LOGGER.info(f"Saving books into {self._last_successful_url_file}")
        file.insert_content_into_file_name(
            self._last_successful_url,
            self._last_successful_url_file
        )
        file.insert_content_into_file_name(
            json.dumps(books, indent=2),
            self.corpus_data_file
        )
        LOGGER.info(f"Total records exported {len(books)}")

    def url_builder(self, **kwargs):
        merged_kwargs = {**DEFAULT_ARGS, **kwargs}
        if "fields" in merged_kwargs:
            merged_kwargs["fields"] = "{{{fields}}}".format(fields=",".join(merged_kwargs["fields"]))
        return self._api_url.format(self.kwargs_to_query_params(**merged_kwargs))

    def filter_by_language(self):
        return {
            language: list(filter(lambda x: x["language"] == language, self._books))
            for language in {x["language"] for x in self._books}
        }

    def export_books_by_language(self):
        for language, books in self.filter_by_language().items():
            file.insert_content_into_file_name(
                json.dumps(books, indent=4),
                os.path.join(
                    self.corpus_folder,
                    f"{language.replace('/','_')}.json"  # This is just to avoid problems with Bisaya/Cebuano
                )
            )
