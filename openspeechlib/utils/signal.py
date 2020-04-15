import numpy as np


def power(signal, axis=-1):
    """
    Calculate the power of a signal using this formula

```latex
E = \sum_{t=0}^{N-1} X^2[t]
```

    Taken from Speech an Language Processing by Dan Jurafsky 2nd edition Chapter 9.3.6
    :param signal:
    :param axis:
    :return:
    """
    return np.sum(np.square(signal), axis=axis)


def replace_zeros_with_almost_zero(signal):
    """
    This function replaces all zeros in a nd array with the non-zero smallest value representable
    :param signal:
    :return:
    """
    return np.where(signal == 0, np.finfo(float).eps, signal)
