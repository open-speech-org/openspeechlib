import os
from unittest import TestCase

import numpy as np
from scipy.io import wavfile

from openspeechlib.utils.windows import extract_overlapping_frames_from_signal
from openspeechlib.feature_extraction.formants import formants


class TestMFCC(TestCase):

    def setUp(self) -> None:
        # For manual testing
        # frequency, signal = wavfile.read("openspeechlib/feature_extraction/tests/agua.wav")
        self.file_path = os.path.join(os.path.dirname(__file__), 'male_a_spa.wav')

    def test_extract_formants(self):

        frequency, signal = wavfile.read(self.file_path)
        extracted_formants = formants(signal, frequency)
        self.assertEqual(extracted_formants.shape, (167, 121))

    def test_step_by_step(self):
        frequency, signal = wavfile.read(self.file_path)
        # The audio was recorded using two channels, so we use just one
        signal = signal[:, 0]
        window_width = int(frequency * 0.025)
        window_offset = int(frequency * 0.01)
        frames = extract_overlapping_frames_from_signal(signal, window_width, window_offset)
        windowed_frames_with_fourier_transform = np.fft.fft(frames)

from scipy import signal
signal.spectrogram()
