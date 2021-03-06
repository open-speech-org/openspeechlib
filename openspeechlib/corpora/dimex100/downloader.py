"""
Implementation to get LibriVox audios
"""
import logging
import zipfile

from openspeechlib.corpora import (
    base,
    exceptions
)

LOGGER = logging.getLogger(__name__)


class Downloader(base.BaseCorpusDownloader):
    corpus_name = "dimex100"
    CORPUS_ONLY_SUPPORTS_FETCH_ALL_CONTENT = "This corpus only supports download all the content"
    source_url = "http://turing.iimas.unam.mx/~luis/DIME/DIMEx100/DVD/DVDCorpusDimex100.zip"

    def fetch_all(self, remember_cache=True):
        zip_location = f"{self.corpus_folder}.zip"


    def fetch(self, _from, _to, **kwargs):
        raise exceptions.ActionNotSupportedException(self.CORPUS_ONLY_SUPPORTS_FETCH_ALL_CONTENT)

