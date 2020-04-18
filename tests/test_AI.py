# Import modules
import sklearn
import joblib

# Import from package
from src.AI import AI


# ===== Test functions for AI ===== #

def test_lecture_modele():
    """Test if [...]"""
    ai = AI(None, None, None, None)
    assert AI.lecture_modele() is None
