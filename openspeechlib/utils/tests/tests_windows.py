from unittest import TestCase

import numpy as np

from openspeechlib.utils import windows


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


class TestFrames(TestCase):
    def setUp(self) -> None:
        self.signal = np.arange(0, 10)

    def test_5_x_3(self):
        self.assertEqual(
            windows.extract_overlapping_frames_from_signal(self.signal, 5, 3).shape,
            (4, 5)
        )

    def test_5_x_4(self):
        self.assertEqual(
            windows.extract_overlapping_frames_from_signal(self.signal, 5, 4).shape,
            (3, 5)
        )

    def test_3_x_1(self):
        self.assertEqual(
            windows.extract_overlapping_frames_from_signal(self.signal, 3, 1).shape,
            (10, 3)
        )

    def test_100_x_5(self):
        self.assertEqual(
            windows.extract_overlapping_frames_from_signal(np.arange(0, 100), 10, 5).shape,
            (20, 10)
        )


class TestApplyFunctionToFrames(TestCase):

    def test_apply_window_function_to_frames_1d_array(self):
        with self.assertRaises(ValueError):
            windows.apply_window_function_to_frames(np.arange(0, 10))

    def test_keep_shape(self):
        array_2D = np.arange(0,25).reshape((5,5))
        self.assertEqual(
            array_2D.shape,
            windows.apply_window_function_to_frames(array_2D).shape
        )
