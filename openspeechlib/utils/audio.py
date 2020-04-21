"""
Utility functions to extract information from audio
"""
import logging

from scipy.io import wavfile
from sphfile import SPHFile

LOGGER = logging.getLogger(__name__)


def get_length_of_wav_wile(wav_path):
    """
    Extracts the duration of a wav file in seconds
    :param wav_path:
    :return:
    """
    try:
        frequency, signal = wavfile.read(wav_path)
        return signal.shape[0] / frequency
    except FileNotFoundError:
        LOGGER.error("File not found")


def get_length_of_sph_file(sph_path):
    """
    Extracts the duration of a sph file in seconds

```python
import pathlib

from openspeechlib.utils.audio import get_length_of_sph_file

total_length_of_ciempiess = 0
for path in pathlib.Path('/mnt/16810535-988c-440c-a794-1c9b98899844/master_thesis/corpus/02_CIEMPIESS_SPH/train').rglob('*.sph'):
    total_length_of_ciempiess += get_length_of_sph_file(path.absolute())

print(total_length_of_ciempiess)
```
    :param sph_path:
    :return:
    """
    try:
        sph_file = SPHFile(sph_path)
        sph_file.open()
        return sph_file.format['sample_count']/sph_file.format['sample_rate']
    except FileNotFoundError:
        LOGGER.error("File not found")
