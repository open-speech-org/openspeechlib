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
    def fetch(self, _from, _to):
        raise NotImplementedError("All BaseCorpus Subclasses must implement the fetch method")
