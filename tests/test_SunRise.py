# Import modules
import numpy as np

# Import from package
from src.SunRise import SunRise


# ===== Test functions for SunRise ===== #


def test_exemple():
    """Test if 2x3=6"""
    sunrise = SunRise(None)
    a, b = 2, 3
    c = a * b
    assert c == 6
