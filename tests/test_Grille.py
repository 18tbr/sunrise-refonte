# Import modules
import numpy as np
import googlemaps

# Import from package
from src.Grille import Grille, Noeud


# ===== Test functions for Grille ===== #

def test_creer_maille():
    """Test if [...]"""
    grille = Grille(None)
    assert Grille.creer_maille() is None


# ===== Test functions for Noeud  ===== #

def test_mettre_a_jour():
    """Test if [...]"""
    noeud = Noeud(None, None)
    assert Noeud.mettre_a_jour(None) is None
