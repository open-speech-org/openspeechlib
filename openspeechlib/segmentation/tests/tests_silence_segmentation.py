import os
from unittest import TestCase

import numpy as np
from scipy.io import wavfile

from openspeechlib.feature_extraction.utils.delta import delta
from openspeechlib.segmentation.silence_segmentation import silence_segmentation
from openspeechlib.utils.windows import extract_overlapping_frames_from_signal, apply_window_function_to_frames
from openspeechlib.utils.signal import power


class TestSilenceSegmentation(TestCase):

    def setUp(self) -> None:
        # For manual testing
        # frequency, signal = wavfile.read("openspeechlib/segmentation/tests/vocales.wav")
        self.file_path = os.path.join(os.path.dirname(__file__), 'vocales.wav')

    def test_segmentation(self):
        frequency, signal = wavfile.read(self.file_path)
        audio_segments = silence_segmentation(signal, frequency)
        self.assertEqual(len(list(audio_segments)), 6)

    def test_step_by_step(self):
        frequency, signal = wavfile.read(self.file_path)

        window_width = int(frequency * 0.025)
        windows_offset = int(frequency * 0.01)
        threshold = 0.03
        frames = extract_overlapping_frames_from_signal(
            signal,
            window_width,
            windows_offset
        )
        windowed_frames = apply_window_function_to_frames(frames)
        energy = power(windowed_frames, axis=1)
        frame_start_time = np.arange(0, signal.shape[-1], windows_offset)
        interpolated_values = np.interp(np.arange(0, signal.shape[0]), frame_start_time, energy, )
        voice_ranges = np.where(interpolated_values > np.max(interpolated_values) * threshold, 1, 0)
        deltas = delta(voice_ranges, (1, -1))
        changes_to_positive = np.where(deltas > 0)
        changes_to_negative = np.where(deltas < 0)
        self.assertEqual(len(list(zip(changes_to_positive[0], changes_to_negative[0]))), 6)
