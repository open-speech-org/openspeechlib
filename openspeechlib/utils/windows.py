"""
Utility functions for Signal windowing

This will be used as proxy in case we want to implement our custom window functions
"""
import numpy as np
from scipy.signal import windows

hamming = windows.hamming


def apply_window_function_to_frames(frames, window_function=hamming):
    if len(frames.shape) != 2:
        raise ValueError('This functions requires a 2D array')
    window_values = window_function(frames.shape[1])
    return np.apply_along_axis(lambda x: x * window_values, 1, frames)


def calculate_pad_size(signal_length, window_width, window_offset):
    useful_space = signal_length % window_offset
    return int(window_width - useful_space) if useful_space != 0 else window_width - window_offset


def extract_overlapping_frames_from_signal(signal, window_width, window_offset):
    signal_length = signal.shape[-1]
    # We fill the signal to ensure the last frame has the appropriate length
    padding_needed = calculate_pad_size(signal_length, window_width, window_offset)
    padded_signal = np.concatenate(
        (
            signal,
            np.zeros(padding_needed)
        )
    )
    initial_frame_index = np.tile(
        np.arange(0, signal_length, window_offset),
        (window_width, 1)
    ).T
    consecutive_indexes_to_add = np.tile(
        np.arange(0, window_width),
        (initial_frame_index.shape[0], 1)
    )
    frame_indexes = initial_frame_index + consecutive_indexes_to_add

    return padded_signal[frame_indexes]
