import numpy as np

from openspeechlib.feature_extraction.utils.delta import delta
from openspeechlib.utils.signal import power
from openspeechlib.utils.windows import extract_overlapping_frames_from_signal, apply_window_function_to_frames


def default_segmentator(procesed_signal, threshold, **kwargs):
    voice_ranges = np.where(procesed_signal > np.max(procesed_signal) * threshold, 1, 0)
    deltas = delta(voice_ranges, (1, -1))
    changes_to_positive = np.where(deltas > 0)
    changes_to_negative = np.where(deltas < 0)
    return zip(changes_to_positive[0], changes_to_negative[0])


def skip_adjacent_segmentator(procesed_signal, threshold, **kwargs):
    skip_adjacent = int(kwargs.get("skip_adjacent", 0))
    silences_start = list()
    signal_start = list()
    is_silence = True
    threshold_value = np.max(procesed_signal) * threshold
    skipped_segments = 0
    possible_start = 0
    print(threshold_value)
    for index, element in enumerate(procesed_signal):
        if is_silence and element > threshold_value:
            if skipped_segments == 0:
                print("Possible start for signal", index)
                possible_start = index
            skipped_segments += 1
            if skipped_segments > skip_adjacent:
                print(index, element, is_silence, element > threshold_value)
                is_silence = False
                signal_start.append(possible_start)
                possible_start = index
                skipped_segments = 0
                print("1")

                continue
        if not is_silence and element < threshold_value:
            if skipped_segments == 0:
                print("Possible start for silence", index)
                possible_start = index
            skipped_segments += 1
            if skipped_segments > skip_adjacent:
                print(index, element, is_silence, element > threshold_value)
                is_silence = True
                silences_start.append(possible_start)
                possible_start = index
                skipped_segments = 0
                print("2")

    return zip(silences_start, signal_start)


def silence_segmentation(
        signal,
        frequency=16000,
        threshold=0.03,
        window_width_size=0.025,
        windows_offset=0.01,
        segmentator=default_segmentator,
        extra_segmentator_args=None
):
    window_width = int(frequency*window_width_size)
    windows_offset = int(frequency*windows_offset)
    frames = extract_overlapping_frames_from_signal(
        signal,
        window_width,
        windows_offset
    )
    windowed_frames = apply_window_function_to_frames(frames)
    energy = power(windowed_frames, axis=1)
    frame_start_time = np.arange(0, signal.shape[-1], windows_offset)
    interpolated_values = np.interp(np.arange(0, signal.shape[0]), frame_start_time, energy, )
    return segmentator(interpolated_values, threshold)
