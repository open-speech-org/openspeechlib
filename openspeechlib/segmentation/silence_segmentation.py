import numpy as np

from openspeechlib.feature_extraction.utils.delta import delta
from openspeechlib.utils.signal import power
from openspeechlib.utils.windows import extract_overlapping_frames_from_signal, apply_window_function_to_frames


def silence_segmentation(
        signal,
        frequency=16000,
        threshold=0.03
):
    window_width = int(frequency*0.025)
    windows_offset = int(frequency*0.01)
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
    return zip(changes_to_positive[0], changes_to_negative[0])
