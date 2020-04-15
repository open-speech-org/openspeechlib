import numpy as np
from scipy.signal import convolve


def delta(signal, convolution_array=(-1, 0, 1)):
    """
    Calculate the variation of a signal using

```latex
d(t) = \fraq={c(t+1)-c(t-1)}{2}
```
    :param signal:
    :return:
    """
    return convolve(signal, np.array(convolution_array), 'same', 'direct') / len(convolution_array)
