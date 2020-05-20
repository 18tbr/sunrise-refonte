# Tests de la représentation sous forme d'image

import matplotlib.pyplot as plt
import os
import sys

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

from Grille import Grille, Noeud, Feuille, Parallele, Serie

def test_representation_image_complexe():
    Cint = 0.5
    T = list(range(10))
    Text = [1 for i in range(10)]
    Tint = list(range(10))
    Pint = [0 for i in range(10)]
    g = Grille(0.5, T, Text, Tint, Pint)
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
    print("score=", g.score())
    image = g.ecritureImage(largeur=100, hauteur=100)
    R, V, B = image[:,:,0], image[:,:,1], image[:,:,2]
    plt.imshow(image)
    plt.colorbar()
    plt.show()
    plt.imshow(R)
    plt.colorbar()
    plt.show()
    plt.imshow(V)
    plt.colorbar()
    plt.show()
    plt.imshow(B)
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    test_representation_image_complexe()
