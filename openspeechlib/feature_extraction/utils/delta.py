import numpy as np
from scipy.signal import convolve


def delta(signal):
    """
    Calculate the variation of a signal using

```latex
d(t) = \fraq={c(t+1)-c(t-1)}{2}
```
    :param signal:
    :return:
    """
    return convolve(signal, np.array([-1, 0, 1]), 'same', 'direct') / 3
