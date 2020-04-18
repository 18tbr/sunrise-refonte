# Import modules
import matplotlib.pyplot as plt

# Import from package
from src.Animation import Animation


# ===== Test functions for Animation ===== #

def test_exemple():
    """Test if 2x3=6"""
    animation = Animation(None, None)
    a, b = 2, 3
    c = a * b
    assert c == 6
