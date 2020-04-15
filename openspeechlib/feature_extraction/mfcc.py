import numpy as np

from openspeechlib.utils.filters import pre_emphasis
from openspeechlib.utils.windows import extract_overlapping_frames_from_signal, apply_window_function_to_frames
from openspeechlib.utils.signal import power, replace_zeros_with_almost_zero
from openspeechlib.feature_extraction.utils.mel_scale import transform_hz_signal_into_mel_scale_using_triangular_filter_banks
from openspeechlib.feature_extraction.utils.delta import delta


def MFCC(
        signal,
        frequency=16000,
        window_width=int(16000*0.025),
        window_offset=int(16000*0.01),
        number_of_mel_filters=40,
):
    """
    This functions calculates the Mel Frequency Cepstral Coeffients of a signal using the following process

    Signal -> Pre_emphasis ->Window -> DFT -> Mel filterbank -> Log -> iDFT -> Deltas -> MFCCs
                               |                                    ^
                               v                                    |
                            Energy -    -   -   -   -   -   -   -  -|

    Taken from Speech an Language Processing by Dan Jurafsky 2nd edition Chapter 9.3
    :param signal:
    :param frequency:
    :param window_width:
    :param window_offset:
    :param number_of_mel_filters
    :return:
    """
    signal_with_pre_emphasis = pre_emphasis(signal)
    frames = extract_overlapping_frames_from_signal(signal_with_pre_emphasis, window_width, window_offset)
    windowed_frames = apply_window_function_to_frames(frames)
    windowed_frames_with_fourier_transform = np.fft.fft(windowed_frames)
    energy = power(windowed_frames, axis=1)

    mel_frames = transform_hz_signal_into_mel_scale_using_triangular_filter_banks(
        windowed_frames_with_fourier_transform,
        frequency,
        number_of_mel_filters
    )

    mel_frames_without_zeros = replace_zeros_with_almost_zero(mel_frames)

    log_of_mel_frames = np.log(mel_frames_without_zeros)
    inverse_fourier_of_log_frames = np.fft.ifft(log_of_mel_frames)

    first_delta = np.apply_along_axis(delta, 0, inverse_fourier_of_log_frames)
    second_delta = np.apply_along_axis(delta, 0, first_delta)

    return np.concatenate((inverse_fourier_of_log_frames, first_delta, second_delta, energy[np.newaxis].T), axis=1)

