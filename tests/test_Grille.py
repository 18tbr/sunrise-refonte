# Import modules
import numpy as np
import os
import sys

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

from Grille import Grille, Noeud, Feuille, Parallele, Serie

# Test des fonctions sur les noeuds en parallèles


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
    p = f1.ajoutFils(f2, forme="parallele")
    assert p.fils == [f1, f2]
    assert p.parent is None
    assert f1.parent == p
    assert f2.parent == p
    assert p.profondeur == 0
    assert f1.profondeur == 1
    assert f2.profondeur == 1
    assert g.forme == [1, 2]
    assert g.racine is p
    return g, p


def test_ajout_parallele_existant():
    g, p = test_ajout_fils_feuille_parallele()
    f1, f2 = p.fils
    f3 = Feuille()
    p.ajoutFils(f3, index=1)
    assert g.forme == [1, 3]
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
    p2 = f3.ajoutFils(f4, forme="parallele")
    assert type(p2) == Parallele
    assert p2.fils == [f3, f4]
    assert p2.grille is g
    assert f3.parent is p2
    assert f4.parent is p2
    assert p2.parent is p
    assert g.forme == [1, 3, 2]
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
    p = f1.ajoutFils(f2, forme="serie")
    assert type(p) is Serie
    assert p.fils == [f1, f2]
    assert p.parent is None
    assert f1.parent == p
    assert f2.parent == p
    assert len(p.capacites) == 1
    assert g.nbCondensateurs == 2
    assert p.profondeur == 0
    assert f1.profondeur == 1
    assert f2.profondeur == 1
    assert g.forme == [1, 2]
    assert g.racine is p
    return g, p


def test_ajout_serie_existant():
    g, p = test_ajout_fils_feuille_serie()
    f1, f2 = p.fils
    f3 = Feuille()
    p.ajoutFils(f3, index=1)
    assert g.forme == [1, 3]
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
    p2 = f3.ajoutFils(f4, forme="serie")
    assert type(p2) == Serie
    assert p2.fils == [f3, f4]
    assert p2.grille is g
    assert len(p2.capacites) == 1
    assert len(p.capacites) == 2
    assert g.nbCondensateurs == 4
    assert f3.parent is p2
    assert f4.parent is p2
    assert p2.parent is p
    assert g.forme == [1, 3, 2]
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


# Tests mixtes de Parallèle et Série


def test_ajout_serie_sur_parallele():
    g, p = test_ajout_parallele_existant()
    f1, f2, f3 = p.fils
    f4 = Feuille()
    p2 = f3.ajoutFils(f4, forme="serie")
    assert type(p2) == Serie
    assert p2.fils == [f3, f4]
    assert p2.grille is g
    assert len(p2.capacites) == 1
    assert type(p) is Parallele
    assert g.nbCondensateurs == 2
    assert f3.parent is p2
    assert f4.parent is p2
    assert p2.parent is p
    assert g.forme == [1, 3, 2]
    return g, p, p2


def test_ajout_parallele_sur_serie():
    g, p = test_ajout_serie_existant()
    f1, f2, f3 = p.fils
    f4 = Feuille()
    p2 = f3.ajoutFils(f4, forme="parallele")
    assert type(p2) == Parallele
    assert p2.fils == [f3, f4]
    assert p2.grille is g
    assert len(p.capacites) == 2
    assert type(p) is Serie
    assert g.nbCondensateurs == 3
    assert f3.parent is p2
    assert f4.parent is p2
    assert p2.parent is p
    assert g.forme == [1, 3, 2]
    return g, p, p2


def test_complexe_creation():
    g = Grille(None, None, None, None, None)
    f1 = g.racine
    f2 = Feuille()
    sA = f1.ajoutFils(f2, forme="serie")
    f3 = Feuille()
    sA.ajoutFils(f3, index=0)
    f4 = Feuille()
    pB = f1.ajoutFils(f4, forme="parallele")
    f5 = Feuille()
    pB.ajoutFils(f5, index=1)
    f6 = Feuille()
    sC = f2.ajoutFils(f6, forme="serie")
    # Tests de généalogie
    assert g.forme == [1, 3, 5]
    assert g.racine is sA
    assert sA.parent is None
    assert sA.fils == [f3, pB, sC]
    assert pB.parent is sA
    assert f3.parent is sA
    assert sC.parent is sA
    assert pB.fils == [f1, f5, f4]
    assert f1.parent is pB
    assert f5.parent is pB
    assert f4.parent is pB
    assert sC.fils == [f2, f6]
    assert f2.parent is sC
    assert f6.parent is sC
    # Tests sur les capacités
    assert len(sA.capacites) == 2
    assert len(sC.capacites) == 1
    assert g.nbCondensateurs == 4
    return g


def test_complexe_destruction():
    g = test_complexe_creation()
    sA = g.racine
    f3, pB, sC = sA.fils
    f1, f5, f4 = pB.fils
    f2, f6 = sC.fils
    f6t = sC.suppressionFils(0)
    assert f6t is f6
    assert sA.fils == [f3, pB, f6]
    assert f6.parent is sA
    assert g.nbCondensateurs == 3
    assert g.forme == [1, 3, 3]
    sAt = sA.suppressionFils(1)
    assert sAt is sA
    assert len(sA.capacites) == 1
    assert g.nbCondensateurs == 2
    assert sA.fils == [f3, f6]
    assert g.forme == [1, 2]
    # On vérifie aussi que pB et ses fils ont bien été détachés
    assert pB.parent is None
    assert pB.grille is None
    assert f1.grille is None
    assert f5.grille is None
    assert f4.grille is None
    f3t = sA.suppressionFils(1)
    assert f3t is f3
    assert g.racine is f3
    assert f3t.parent is None
    assert g.forme == [1]
    assert g.nbCondensateurs == 1
    return g


# Test de fonctions complexes sur les arbres


def test_inspecter():
    g = test_complexe_creation()
    sA = g.racine
    f3, pB, sC = sA.fils
    f1, f5, f4 = pB.fils
    f2, f6 = sC.fils
    assert g.inspecter(0, 0) is sA
    assert g.inspecter(1, 0) is f3
    assert g.inspecter(1, 1) is pB
    assert g.inspecter(1, 2) is sC
    assert g.inspecter(2, 0) is f1
    assert g.inspecter(2, 1) is f5
    assert g.inspecter(2, 2) is f4
    assert g.inspecter(2, 3) is f2
    assert g.inspecter(2, 4) is f6
    return g


def test_sousArbre():
    g = test_complexe_creation()
    sA = g.racine
    f3, pB, sC = sA.fils
    f1, f5, f4 = pB.fils
    f2, f6 = sC.fils
    # Test de sousArbre sur une feuille
    f3s = f3.sousArbre()
    assert f3s is not f3
    assert f3s.parent is None
    assert f3s.grille is None
    assert f3s.H == f3s.H
    # Test de sousArbre sur une liaison parallèle
    pBs = pB.sousArbre()
    f1s, f5s, f4s = pBs.fils
    assert pBs is not pB
    assert pBs.parent is None
    assert pBs.grille is None
    assert f1s.grille is None
    assert f1s.parent is pBs
    assert f1s.H == f1.H
    assert f5s.grille is None
    assert f5s.parent is pBs
    assert f5s.H == f5.H
    assert f4s.grille is None
    assert f4s.parent is pBs
    assert f4s.H == f4.H
    # Test de sousArbre sur une liaison série
    sCs = sC.sousArbre()
    f2s, f6s = sCs.fils
    assert sCs is not sC
    assert sCs.parent is None
    assert sCs.grille is None
    assert f2s.grille is None
    assert f2s.parent is sCs
    assert f2s.H == f2.H
    assert f6s.grille is None
    assert f6s.parent is sCs
    assert f6s.H == f6.H
    return g

def test_substituer_serie():
    g = test_complexe_creation()
    sA = g.racine
    f3, pB, sC = sA.fils
    f1, f5, f4 = pB.fils
    f2, f6 = sC.fils
    pBr = pB.sousArbre()
    f6r = f6.sousArbre()
    ancienCondensateurs = sA.capacites
    sA.substituerEnfants([f6r, pBr])
    assert sA.fils == [f6r, pBr]
    assert f6r.parent is sA
    assert pBr.parent is sA
    assert f6r.grille is g
    assert pBr.grille is g
    assert sA.capacites == ancienCondensateurs[:1]
    assert g.forme == [1, 2, 3]
    assert g.nbCondensateurs == 2
    return g

def test_substituer_parallele():
    g = test_complexe_creation()
    sA = g.racine
    f3, pB, sC = sA.fils
    f1, f5, f4 = pB.fils
    f2, f6 = sC.fils
    sCr = sC.sousArbre()
    f6r = f6.sousArbre()
    pB.substituerEnfants([f6r, sCr])
    assert pB.fils == [f6r, sCr]
    assert f6r.parent is pB
    assert sCr.parent is pB
    assert f6r.grille is g
    assert sCr.grille is g
    assert g.forme == [1, 3, 4, 2]
    assert g.nbCondensateurs == 5
    return g
