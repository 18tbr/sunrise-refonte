# Import modules
import tkinter as tk

# Import from package
from src.Animation import *
from src.UI import UI


# ===== Test functions for UI ===== #


def test_lecture_parametres():
    """Test if [...]"""
    ui = UI()
    assert UI.lecture_parametres() is None
