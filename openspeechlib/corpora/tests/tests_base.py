from unittest import TestCase

from openspeechlib.corpora.base import BaseCorpus


class TestsBase(TestCase):

    def test_kwargs_to_query_params(self):

        self.assertEqual(
            BaseCorpus.kwargs_to_query_params(a=1, b=2),
            'a=1&b=2'
        )
