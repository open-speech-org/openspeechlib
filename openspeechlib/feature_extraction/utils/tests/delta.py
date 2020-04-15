from unittest import TestCase

import numpy as np

from openspeechlib.feature_extraction.utils import delta


class TestDelta(TestCase):

    def setUp(self) -> None:
        self.delta = delta.delta

    def test_shape_delta(self):
        signal = np.arange(0, 10)
        self.assertEqual(self.delta(signal).shape, (10,))
