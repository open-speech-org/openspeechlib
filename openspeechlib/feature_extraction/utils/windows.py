"""
Utility functions for Signal windowing

This will be used as proxy in case we want to implement our custom window functions
"""
import numpy as np
from scipy.signal import windows

hamming = windows.hamming


def calculate_pad_size(signal_length, window_width, window_offset):
    useful_space = signal_length % window_offset
    return int(window_width - useful_space) if useful_space != 0 else window_offset


def extract_overlapping_frames_from_signal(signal, window_width, window_offset):
    signal_length = signal.shape[-1]
    # We fill the signal to ensure the last frame has the appropriate length
    padded_signal = np.concatenate(
        (
            signal,
            np.zeros(calculate_pad_size(signal_length, window_width, window_offset))
        )
    )
    padded_signal_length = padded_signal.shape[-1]
    initial_frame_index = np.tile(
        np.arange(0, signal_length, window_offset),
        (window_width, 1)
    ).T
    consecutive_indexes_to_add = np.tile(
        np.arange(0, window_width),
        (padded_signal_length//window_offset, 1)
    )
    print(calculate_pad_size(signal_length, window_width, window_offset))
    print(padded_signal)
    print(padded_signal_length)
    print(initial_frame_index)
    print(consecutive_indexes_to_add)
    frame_indexes = initial_frame_index + consecutive_indexes_to_add
    print(frame_indexes)
    return padded_signal[frame_indexes]


extract_overlapping_frames_from_signal(np.arange(0,10), 5,3)
