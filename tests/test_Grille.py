# Import modules
import numpy as np
import os
import sys
# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")
# Import from package
from Grille import Grille, Noeud, Feuille, Parallele, Serie


# ===== Test functions for Grille ===== #


# def test_creer_maille():
#     """Test if [...]"""
#     grille = Grille(None)
#     assert Grille.creer_maille() is None


# ===== Test functions for Noeud  ===== #


def test_creation_arbre_minimal():
    """Test if [...]"""
    g = Grille(None, None, None, None, None)
    assert g.forme == [1]
    f = g.racine
    assert f.grille == g
    assert f.parent is None
    g.racine = f
    assert f.profondeur == 0
    assert g.forme == [1]
    return g, f

def test_ajout_fils_feuille_parallele():
    g, f1 = test_creation_arbre_minimal()
    f2 = Feuille(None)
    p = f1.ajoutFils(f2, forme='parallele')
    assert p.fils == [f1,f2]
    assert p.parent is None
    assert f1.parent == p
    assert f2.parent == p
    assert p.profondeur == 0
    assert f1.profondeur == 1
    assert f2.profondeur == 1
    assert g.forme == [1, 2]
    return g, p

def test_ajout_parallele_existant():
    g, p = test_ajout_fils_feuille_parallele()
    f1, f2 = p.fils
    f3 = Feuille(None)
    p.ajoutFils(f3, index=1)
    assert g.forme == [1,3]
    assert f3.grille is g
    assert f3.parent is p
    assert p.fils == [f1, f3, f2]
    return g, p

def test_suppression_fils_parallele_simple():
    g, p = test_ajout_parallele_existant()
    f1, f2, f3 = p.fils
    pn = p.suppressionFils(2)
    assert pn is p
    assert g.forme == [1, 2]
    assert p.fils == [f1, f2]
    return g, p

def test_suppression_parallele_dernier():
    g, p = test_ajout_fils_feuille_parallele()
    f1, f2 = p.fils
    pn = p.suppressionFils(0)
    assert g.forme == [1]
    assert pn is f2
    return g, f2
