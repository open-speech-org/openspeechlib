import numpy as np

from openspeechlib.utils.windows import extract_overlapping_frames_from_signal


def formants(
        signal,
        frequency=16000,
        window_width=int(16000 * 0.025),
        window_offset=int(16000 * 0.01),
        number_of_formants=3
):
    """
    This function extract the formats in a given signal using a Fourier Transform over a set of overlapping frames
    and returning the first number of formants in each frame using the firsts  local maximum on the spectral domain
    :param signal:
    :param frequency:
    :param window_width:
    :param window_offset:
    :return:
    """
    frames = extract_overlapping_frames_from_signal(signal, window_width, window_offset)
    windowed_frames_with_fourier_transform = np.fft.fft(frames)
