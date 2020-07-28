import numpy as np

from openspeechlib.feature_extraction.utils.delta import delta
from openspeechlib.utils.signal import power
from openspeechlib.utils.windows import extract_overlapping_frames_from_signal, apply_window_function_to_frames


def default_segmentator(procesed_signal, threshold, **kwargs):
    frequency = int(kwargs.get("frequency", 16000))
    voice_ranges = np.where(procesed_signal > np.max(procesed_signal) * threshold, 1, 0)
    deltas = delta(voice_ranges, (1, -1))
    changes_to_positive = np.where(deltas > 0)
    changes_to_negative = np.where(deltas < 0)
    return zip(changes_to_positive[0]*frequency, changes_to_negative[0]*frequency)


def skip_adjacent_segmentator(procesed_signal, threshold, **kwargs):
    skip_adjacent = int(kwargs.get("skip_adjacent", 10))
    min_silence_gap = float(kwargs.get("min_silence_gap", 0.5))
    windows_offset_size = float(kwargs.get("windows_offset_size", 0.01))
    frequency = int(kwargs.get("frequency", 16000))
    silences_start = list()
    signal_start = list()
    is_silence = True
    threshold_value = np.max(procesed_signal) * threshold
    skipped_segments = 0
    possible_start = 0
    print(threshold_value)
    index = 0
    max_iterations = len(procesed_signal) * 5
    iteration = 0
    while index < len(procesed_signal) and iteration < max_iterations:
        element = procesed_signal[index]
        index += 1
        max_iterations += 1
        if is_silence and element > threshold_value:
            if skipped_segments == 0:
                possible_start = index
            skipped_segments += 1
            if skipped_segments > skip_adjacent:
                is_silence = False
                signal_start.append(possible_start)
                index = possible_start
                skipped_segments = 0
                continue
        if not is_silence and element < threshold_value:
            if skipped_segments == 0:
                possible_start = index
            skipped_segments += 1
            if skipped_segments > skip_adjacent:
                is_silence = True
                silences_start.append(possible_start)
                index = possible_start
                skipped_segments = 0
    silence_gap_size = min_silence_gap / windows_offset_size
    silence_gaps = list()
    for index in range(len(signal_start) - 1):
        if signal_start[index + 1] - silences_start[index] > silence_gap_size:
            silence_gaps.append((
                silences_start[index] * frequency * windows_offset_size,
                signal_start[index + 1] * frequency * windows_offset_size))
    return silence_gaps


def silence_segmentation(
        signal,
        frequency=16000,
        threshold=0.03,
        window_width_size=0.025,
        windows_offset_size=0.01,
        segmentator=default_segmentator,
        extra_segmentator_args=None
):
    if extra_segmentator_args is None:
        extra_segmentator_args = dict()
    window_width = int(frequency*window_width_size)
    windows_offset = int(frequency*windows_offset_size)
    frames = extract_overlapping_frames_from_signal(
        signal,
        window_width,
        windows_offset
    )
    windowed_frames = apply_window_function_to_frames(frames)
    energy = power(windowed_frames, axis=1)
    # I think I don't need interpolate
    # Instead I can multiply the values of the energy with the step size
    # frame_start_time = np.arange(0, signal.shape[-1], windows_offset)
    # interpolated_values = np.interp(np.arange(0, signal.shape[0]), frame_start_time, energy, )
    return segmentator(
        energy,
        threshold,
        **{
            **extra_segmentator_args,
            **{
                "frequency": frequency,
                "window_width_size": window_width_size,
                "windows_offset_size": windows_offset_size,
            }
        }
    )
