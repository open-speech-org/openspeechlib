"""
All base functionality to download corpus
"""
from abc import ABCMeta, abstractmethod

CORPORA_FOLDER = ".openspeechlib/corpora"
LAST_FETCHED_URL = "{}_last_fetched_url.txt"
MAX_REQUESTS = 100
PAGE_SIZE = 50


class BaseCorpus(metaclass=ABCMeta):
    _api_url = None
    _format = None
    _node_text = None
    _node_identifier = None
    _arg_pagination = None

    @property
    @abstractmethod
    def corpus_name(self):
        raise NotImplementedError("All BaseCorpus Subclasses must implement the corpus_name attribute")

    @abstractmethod
    def fetch_all(self, remember_cache=True):
        raise NotImplementedError("All BaseCorpus Subclasses must implement the fetch_all method")

    @abstractmethod
    def fetch(self, _from, _to, **kwargs):
        raise NotImplementedError("All BaseCorpus Subclasses must implement the fetch method")

    def url_builder(self, **kwargs):
        return self._api_url.format(**kwargs)

    @staticmethod
    def kwargs_to_query_params(**kwargs):
        return "&".join([f"{key}={value}" for key, value in kwargs.items()])
