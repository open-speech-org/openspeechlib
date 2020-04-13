import numpy as np

from openspeechlib.feature_extraction.utils.filters import pre_emphasis


def MFCC(
        signal,
        frequency=16000,
        window_width=16000*0.025,
        window_offset=16000*0.01
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
    :return:
    """
    signal_with_pre_emphasis = pre_emphasis(signal)
