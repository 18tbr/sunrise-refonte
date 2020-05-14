# Import modules
import numpy as np
import os
import sys
# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")
# Import from package
from Grille import Grille, Noeud, Feuille, Parallele, Serie


# ===== Fonctions de test pour Grille ===== #


# def test_creer_maille():
#     """Test if [...]"""
#     grille = Grille(None)
#     assert Grille.creer_maille() is None


# ===== Fonctions de test pour Noeud  ===== #

# Test des fonctions sur les noeuds en parallèle

def test_creation_arbre_minimal():
    """Test if [...]"""
    g = Grille(None, None, None, None, None)
    assert g.forme == [1]
    f = g.racine
    assert f.grille == g
    assert f.parent is None
    assert f.profondeur == 0
    assert g.forme == [1]
    return g, f

def test_ajout_fils_feuille_parallele():
    g, f1 = test_creation_arbre_minimal()
    f2 = Feuille()
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
    f3 = Feuille()
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

def test_ajout_parallele_existant_rang_superieur():
    g, p = test_ajout_parallele_existant()
    f1, f2, f3 = p.fils
    f4 = Feuille()
    p2 = f3.ajoutFils(f4, forme='parallele')
    assert type(p2) == Parallele
    assert p2.fils == [f3, f4]
    assert p2.grille is g
    assert f3.parent is p2
    assert f4.parent is p2
    assert p2.parent is p
    assert g.forme == [1,3,2]
    return g, p, p2

def test_suppression_parallele_existant_rang_superieur():
    g, p, p2 = test_ajout_parallele_existant_rang_superieur()
    f3, f4 = p2.fils
    f = p2.suppressionFils(1)
    assert f is f3
    assert f.grille is g
    assert f3.parent is p
    assert g.forme == [1, 3]
    return g, p

# Test des fonctions pour les noeuds Serie

def test_ajout_fils_feuille_serie():
    g, f1 = test_creation_arbre_minimal()
    f2 = Feuille()
    p = f1.ajoutFils(f2, forme='serie')
    assert type(p) is Serie
    assert p.fils == [f1,f2]
    assert p.parent is None
    assert f1.parent == p
    assert f2.parent == p
    assert len(p.capacites) == 1
    assert g.nbCondensateurs == 2
    assert p.profondeur == 0
    assert f1.profondeur == 1
    assert f2.profondeur == 1
    assert g.forme == [1, 2]
    return g, p

def test_ajout_serie_existant():
    g, p = test_ajout_fils_feuille_serie()
    f1, f2 = p.fils
    f3 = Feuille()
    p.ajoutFils(f3, index=1)
    assert g.forme == [1,3]
    assert f3.grille is g
    assert f3.parent is p
    assert p.fils == [f1, f3, f2]
    assert len(p.capacites) == 2
    assert g.nbCondensateurs == 3
    return g, p

def test_suppression_fils_serie_simple():
    g, p = test_ajout_serie_existant()
    f1, f2, f3 = p.fils
    pn = p.suppressionFils(2)
    assert pn is p
    assert g.forme == [1, 2]
    assert p.fils == [f1, f2]
    assert len(p.capacites) == 1
    assert g.nbCondensateurs == 2
    return g, p

def test_suppression_serie_dernier():
    g, p = test_ajout_fils_feuille_serie()
    f1, f2 = p.fils
    pn = p.suppressionFils(0)
    assert g.forme == [1]
    assert pn is f2
    assert g.nbCondensateurs == 1
    return g, f2


def test_ajout_serie_existant_rang_superieur():
    g, p = test_ajout_serie_existant()
    f1, f2, f3 = p.fils
    f4 = Feuille()
    p2 = f3.ajoutFils(f4, forme='serie')
    assert type(p2) == Serie
    assert p2.fils == [f3, f4]
    assert p2.grille is g
    assert len(p2.capacites) == 1
    assert len(p.capacites) == 2
    assert g.nbCondensateurs == 4
    assert f3.parent is p2
    assert f4.parent is p2
    assert p2.parent is p
    assert g.forme == [1,3,2]
    return g, p, p2

def test_suppression_serie_existant_rang_superieur():
    g, p, p2 = test_ajout_serie_existant_rang_superieur()
    f3, f4 = p2.fils
    f = p2.suppressionFils(1)
    assert f is f3
    assert f.grille is g
    assert f3.parent is p
    assert g.forme == [1, 3]
    assert len(p.capacites) == 2
    assert g.nbCondensateurs == 3
    return g, p
