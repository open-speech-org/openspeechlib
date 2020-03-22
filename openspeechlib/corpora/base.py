"""
All base functionality to download corpus
"""
from abc import ABCMeta, abstractmethod


class BaseCorpus(metaclass=ABCMeta):
    _api_url = None
    _format = None
    _node_text = None
    _node_identifier = None
    _arg_pagination = None

    @abstractmethod
    def fetch(self, _from=None, _to=None, **kwargs):
        raise NotImplementedError("All BaseCorpus Subclasses must implement the fetch method")

    def url_builder(self, **kwargs):
        return self._api_url.format(**kwargs)

    @staticmethod
    def kwargs_to_query_params(**kwargs):
        return "&".join([f"{key}={value}" for key, value in kwargs.items()])
