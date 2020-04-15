import numpy as np


def pre_emphasis(signal, alpha=0.9):
    """
    Implements a first-order high-pass filter for a signal in the time domain using the following equation

```latex
y[n] = x[n] - \alpha x[n-1] | 0.9 \le \alpha \le 1.0
```

Taken from Speech an Language Processing by Dan Jurafsky 2nd edition Chapter 9.3.1
    :param signal:
    :param alpha:
    :return:
    """
    return np.append(signal[0], signal[1:] - alpha*signal[:-1])


def triangular_filter_bank(bins, number_of_filters, signal_size):
    """
    Implements a triangular filter to be used as filterbank defined by:

```latex
H_m[k]= \left\{ \begin{array}{lc}
  0  & k \lt f[m-1] \\
  \frac{k-f[m-1]}{f[m]-f[m-1]} & f[m-1] \le k \le f[m] \\
  \frac{f[m+1]-k}{f[m+1]-f[m]} & f[m] \le k \le f[m+1] \\
  0 & k > f[m+1]
```

Taken from Spoken Language Processing by Xuedong Huang Chapter 6.5.2
    :param bins Array with the bin frequency representation
    :param number_of_filters Number of filters to check
    :return:
    """
    filter_bank = np.zeros([number_of_filters, signal_size])  # This filter bank represents H in our formula
    for m in range(number_of_filters):
        for k in range(int(bins[m]), int(bins[m + 1])):
            filter_bank[m, k] = (k - bins[m]) / (bins[m + 1] - bins[m])
        for k in range(int(bins[m + 1]), int(bins[m + 2])):
            filter_bank[m, k] = (bins[m + 2] - k) / (bins[m + 2] - bins[m + 1])
    return filter_bank
