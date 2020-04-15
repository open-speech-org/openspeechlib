import numpy as np

from openspeechlib.utils.filters import triangular_filter_bank

def hz_to_mel(f):
    """
    Transform a frequency f into the Mel Scale

    Taken from Speech an Language Processing by Dan Jurafsky 2nd edition Chapter 9.3.4
    :param f:
    :return:
    """
    return 1127 * np.log(1+f/700)


def mel_to_hz(m):
    """
    Transform a mel into the frequency scale
    :param m:
    :return:
    """
    return 700 * (np.e**(m/1127) -1)


def transform_hz_signal_into_mel_scale_using_triangular_filter_banks(signal, frequency, number_of_mel_filters):
    """
    Transform a hz signal into a mel coefficients using triangular filters using a scaled triangular filter
    :param signal:
    :param frequency:
    :param number_of_mel_filters:
    :return:
    """
    lower_mel_frequency = 0
    highest_mel_frequency = hz_to_mel(frequency / 2)
    mel_bins = np.linspace(lower_mel_frequency, highest_mel_frequency, number_of_mel_filters + 2)
    hz_bins = mel_to_hz(mel_bins)
    signal_size = signal.shape[-1]
    mel_points = np.floor(signal_size * hz_bins / frequency)
    filter_bank = triangular_filter_bank(mel_points, number_of_mel_filters, signal_size)
    return np.dot(signal, filter_bank.T)
