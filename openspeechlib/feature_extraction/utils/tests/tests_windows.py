from unittest import TestCase

from openspeechlib.feature_extraction.utils import windows


class TestsWindows(TestCase):

    def setUp(self) -> None:
        self.frequency = 16000
        self.window_width = 16000 * 0.025
        self.window_offset = 16000 * 0.01

    def test_desktop_1(self):
        self.assertEqual(windows.calculate_pad_size(10, 5, 3), 4)

    def test_desktop_2(self):
        self.assertEqual(windows.calculate_pad_size(10, 5, 4), 3)

    def test_desktop_3(self):
        self.assertEqual(windows.calculate_pad_size(10, 3, 1), 2)


    def test_incomplete_window_padding_multiple(self):
        total_signal_length = 100
        self.assertEqual(windows.calculate_pad_size(total_signal_length, 10, 5), 5)
