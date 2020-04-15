import os
from unittest import TestCase

import numpy as np
from scipy.io import wavfile

from openspeechlib.utils.filters import pre_emphasis, triangular_filter_bank
from openspeechlib.utils.windows import extract_overlapping_frames_from_signal, hamming
from openspeechlib.feature_extraction.utils.mel_scale import hz_to_mel, mel_to_hz
from openspeechlib.feature_extraction.utils.delta import delta
from openspeechlib.feature_extraction.mfcc import MFCC


class TestMFCC(TestCase):

    def setUp(self) -> None:
        # For manual testing
        # frequency, signal = wavfile.read("openspeechlib/feature_extraction/tests/agua.wav")
        self.file_path = os.path.join(os.path.dirname(__file__), 'agua.wav')

    def test_extract_mfcc(self):

        frequency, signal = wavfile.read(self.file_path)
        mfccs = MFCC(signal, frequency)
        self.assertEqual(mfccs.shape, (167, 121))

    def test_step_by_step(self):
        frequency, signal = wavfile.read(self.file_path)
        window_width = int(frequency * 0.025)
        window_offset = int(frequency * 0.01)
        number_of_mel_filters = 40
        signal_with_pre_emphasis = pre_emphasis(signal)
        frames = extract_overlapping_frames_from_signal(signal_with_pre_emphasis, window_width, window_offset)
        hamming_frame = hamming(window_width)
        windowed_frames = np.apply_along_axis(lambda x: x * hamming_frame, 1, frames)
        windowed_frames_with_fourier_transform = np.fft.fft(windowed_frames)
        energy = np.sum(np.square(windowed_frames), axis=1)
        lower_mel_frequency = 0
        highest_mel_frequency = hz_to_mel(frequency / 2)
        mel_bins = np.linspace(lower_mel_frequency, highest_mel_frequency, number_of_mel_filters + 2)
        hz_bins = mel_to_hz(mel_bins)

        signal_size = windowed_frames_with_fourier_transform.shape[-1]

        mel_points = np.floor(signal_size * hz_bins / frequency)
        filter_bank = triangular_filter_bank(mel_points, number_of_mel_filters, signal_size)
        mel_frames = np.dot(windowed_frames_with_fourier_transform, filter_bank.T)

        mel_frames_without_zeros = np.where(mel_frames == 0, np.finfo(float).eps, mel_frames)

        log_of_mel_frames = np.log(mel_frames_without_zeros)
        inverse_fourier_of_log_frames = np.fft.ifft(log_of_mel_frames)

        first_delta = np.apply_along_axis(delta, 0, inverse_fourier_of_log_frames)
        second_delta = np.apply_along_axis(delta, 0, first_delta)

        self.assertEqual(np.concatenate((inverse_fourier_of_log_frames, first_delta, second_delta, energy[np.newaxis].T), axis=1).shape, (167,121))
