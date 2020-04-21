import os
from unittest import TestCase

from openspeechlib.utils import audio


class TestAudioLength(TestCase):

    def test_audio_wav_length(self):
        file_path = os.path.join(os.path.dirname(__file__), 'male_a_spa.wav')
        self.assertAlmostEqual(
            audio.get_length_of_wav_wile(file_path),
            1.0,
            2
        )

    def test_audio_sph_length(self):
        file_path = os.path.join(os.path.dirname(__file__), '0001M_01ALX_20AGO12.sph')
        self.assertAlmostEqual(
            audio.get_length_of_sph_file(file_path),
            5.0,
            0
        )
