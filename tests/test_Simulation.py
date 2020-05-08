# Import modules
import numpy as np
from scipy.integrate import odeint

# Import from package
from src.Simulation import Simulation


# ===== Test functions for Simulation ===== #


def test_exemple():
    """Test if 2x3=6"""
    simulation = Simulation(None, None)
    a, b = 2, 3
    c = a * b
    assert c == 6
