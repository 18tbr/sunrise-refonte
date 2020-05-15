# Import modules
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")
# Import from package
from Grille import Grille, Noeud, Feuille, Parallele, Serie


# ===== Test functions for Simulation ===== #


def test_creationSimulation_minimal():
    Cint = 0.5
    T = list(range(10))
    Text = [1 for i in range(10)]
    Tint = list(range(10))
    Pint = [0 for i in range(10)]
    g = Grille(0.5, T, Text, Tint, Pint)
    f = g.racine
    A, B, C = g.creationSimulation()
    assert np.shape(A) == (1, 1)
    assert A[0, 0] == f.H
    assert np.shape(C) == (1, 1)
    assert C[0, 0] == 2
    assert np.shape(B) == (1, 2)
    assert B[0, 0] == -f.H
    assert B[0, 1] == 1
    return g


def test_creationSimulation_parallele_simple():
    Cint = 0.5
    T = list(range(10))
    Text = [1 for i in range(10)]
    Tint = list(range(10))
    Pint = [0 for i in range(10)]
    g = Grille(0.5, T, Text, Tint, Pint)
    f1 = g.racine
    f2 = Feuille()
    p = f1.ajoutFils(f2, forme='parallele')
    f3 = Feuille()
    p.ajoutFils(f3, index=2)
    A, B, C = g.creationSimulation()
    assert np.shape(A) == (1, 1)
    assert A[0, 0] == f1.H + f2.H + f3.H
    assert np.shape(C) == (1, 1)
    assert C[0, 0] == 2
    assert np.shape(B) == (1, 2)
    assert B[0, 0] == -(f1.H + f2.H + f3.H)
    assert B[0, 1] == 1
    return g


def test_creationSimulation_serie_simple():
    cInt = 0.5
    T = np.array(list(range(10)))
    tExt = np.array([1 for i in range(10)])
    tInt = np.array(list(range(10)))
    pInt = np.array([0 for i in range(10)])
    g = Grille(cInt, T, tExt, tInt, pInt)
    f1 = g.racine
    f2 = Feuille()
    p = f1.ajoutFils(f2, forme='serie')
    f3 = Feuille()
    p.ajoutFils(f3, index=2)
    c1, c2 = p.capacites
    A, B, C = g.creationSimulation()
    assert (A == np.array([[f3.H, 0, -f3.H], [0, f1.H + f2.H, -f2.H], [-f3.H, -f2.H, f2.H + f3.H]])).all()
    assert (C == np.array([[1/cInt, 0, 0], [0, 1/c1, 0], [0, 0, 1/c2]])).all()
    print(B)
    assert (B == np.array([[0, 1], [-f1.H, 0], [0, 0]])).all()
    return g


def test_creationSimulation_complexe():
    cInt = 0.5
    T = [float(i) for i in range(10)]
    tExt = [1 for i in range(10)]
    tInt = list(range(10))
    pInt = [0 for i in range(10)]
    g = Grille(cInt, T, tExt, tInt, pInt)
    f1 = g.racine
    f2 = Feuille()
    sA = f1.ajoutFils(f2, forme='serie')
    f3 = Feuille()
    sA.ajoutFils(f3, index=2)
    f4 = Feuille()
    pB = f3.ajoutFils(f4, forme='parallele')
    f5 = Feuille()
    sC = f3.ajoutFils(f5, forme='serie')
    f6 = Feuille()
    sC.ajoutFils(f6, index=0)
    f7 = Feuille()
    sD = f2.ajoutFils(f7, forme='serie')
    f8 = Feuille()
    pE = f2.ajoutFils(f8, forme='parallele')
    f9 = Feuille()
    pE.ajoutFils(f9, index=2)
    # Oui, c'est un exemple assez compliqué, c'est parce que j'essaie de tester l'implémentation de curseur, qui n'intervient que dans des cas assez importants.
    cA, cB = sA.capacites
    cC = sD.capacites[0]
    cD, cE = sC.capacites
    # Pour proposer les solutions qui suivent j'ai suivi l'algorithme à la main sur un tableau.
    solA = np.array([[f4.H + f5.H, 0, -f4.H, 0, 0, -f5.H],
                     [0, f1.H + f2.H + f8.H + f9.H, 0, -f2.H -f8.H - f9.H, 0, 0],
                     [-f4.H, 0, f4.H + f6.H + f7.H, -f7.H, -f6.H, 0],
                     [0, -f2.H -f8.H - f9.H, -f7.H, f2.H + f7.H +f8.H +f9.H, 0,0],
                     [0,0,-f6.H,0,f3.H+f6.H,-f3.H],
                     [-f5.H,0,0,0, -f3.H, f3.H + f5.H]])
    solB = np.array([[0,1],[-f1.H,0],[0,0],[0,0],[0,0],[0,0]])
    solC = np.diag([1/cInt, 1/cA, 1/cB, 1/cC, 1/cD, 1/cE])
    A, B, C = g.creationSimulation()
    assert (A == solA).all()
    assert (B == solB).all()
    assert (C == solC).all()
    return g

def test_simulation_coherence():
    cInt = 0.5
    T = list(range(10))
    tExt = [1 for i in range(10)]
    tInt = list(range(10))
    pInt = [0 for i in range(10)]
    g = Grille(cInt, T, tExt, tInt, pInt)
    f1 = g.racine
    f2 = Feuille()
    sA = f1.ajoutFils(f2, forme='serie')
    f3 = Feuille()
    sA.ajoutFils(f3, index=2)
    f4 = Feuille()
    pB = f3.ajoutFils(f4, forme='parallele')
    f5 = Feuille()
    sC = f3.ajoutFils(f5, forme='serie')
    f6 = Feuille()
    sC.ajoutFils(f6, index=0)
    f7 = Feuille()
    sD = f2.ajoutFils(f7, forme='serie')
    f8 = Feuille()
    pE = f2.ajoutFils(f8, forme='parallele')
    f9 = Feuille()
    pE.ajoutFils(f9, index=2)
    sol = g.simulation()
    x, y = sol.t, sol.y[0]
    assert sol.success
    assert (x == np.array(T)).all()
    for temperature in sol.y:
        assert temperature[0] == tExt[0]
    assert len(x) == len(y)
    # C'est à peu près tout ce que l'on peut vérifier simplement sur la cohérence de la simulation...
    return g
