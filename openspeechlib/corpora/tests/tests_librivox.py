from unittest import TestCase

from openspeechlib.corpora.librivox import LibriVox, SLIM_FIELDS


class TestsLibriVox(TestCase):

    def setUp(self) -> None:
        self.librivox = LibriVox()

    def test_default_url_builder(self):
        self.assertEqual(
            self.librivox.url_builder(),
            self.librivox._api_url.format("format=json&limit=50&offset=0")
        )

    def test_url_builder_custom_offset(self):
        self.assertEqual(
            self.librivox.url_builder(offset=100),
            self.librivox._api_url.format("format=json&limit=50&offset=100")
        )

    def test_url_builder_SLIM_FIELDS(self):
        self.assertEqual(
            self.librivox.url_builder(fields=SLIM_FIELDS),
            self.librivox._api_url.format("format=json&limit=50&offset=0&fields={id,title,url_text_source,language,url_zip_file,totaltimesecs,url_librivox}")
        )
