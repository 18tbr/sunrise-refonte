# Tests de la représentation sous forme d'image

import matplotlib.pyplot as plt
import os
import sys
from math import log
import numpy as np

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

from Grille import Grille, Noeud, Feuille, Parallele, Serie, SimulationException
import Coefficients


def test_representation_image_complexe():
    len = 30
    Cint = Coefficients.muC
    T = list(range(len))
    Text = list(range(len))
    Tint = [-1.4 * (i / len) for i in range(len)]
    Pint = [0 for i in range(len)]
    # scores = []
    iterations = 100
    # compteur = 0
    # for i in range(iterations):
    #     try:
    #         g = Grille(Cint, T, Text, Tint, Pint)
    #         f1 = g.racine
    #         f2 = Feuille()
    #         sA = f1.ajoutFils(f2, forme="serie")
    #         f3 = Feuille()
    #         sA.ajoutFils(f3, index=0)
    #         f4 = Feuille()
    #         pB = f1.ajoutFils(f4, forme="parallele")
    #         f5 = Feuille()
    #         pB.ajoutFils(f5, index=1)
    #         f6 = Feuille()
    #         sC = f2.ajoutFils(f6, forme="serie")
    #         scores.append(g.score())
    #         compteur+=1
    #         print("score=", scores[-1])
    #     except SimulationException as e:
    #         print(str(e))
    # plt.plot(range(50), sorted(scores)[-50:])
    # plt.show()
    # dist = []
    for i in range(iterations):
        g = Grille(Cint, T, Text, Tint, Pint)
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
        image = g.ecritureImage(largeur=100, hauteur=100)
        print("(1) score=", g.score())
        ancienneImage = image.copy()
        # R, V, B = image[:,:,0], image[:,:,1], image[:,:,2]
        # plt.imshow(image)
        # plt.show()
        # plt.imshow(R)
        # plt.colorbar()
        # plt.show()
        # plt.imshow(V)
        # plt.colorbar()
        # plt.show()
        # plt.imshow(B)
        # plt.colorbar()
        # plt.show()
        g.lectureImage(image)
        # print(i)
        print("(2) score=", g.score())
        print()
        # image2 = g.ecritureImage(largeur=100, hauteur=100)
        # g.lectureImage(image2.copy())
        # print("(3) score=", g.score())
        # image3 = g.ecritureImage(largeur=100, hauteur=100)
        # g.lectureImage(image3.copy())
        # print("(4) score=", g.score())
        # image = g.ecritureImage(largeur=100, hauteur=100)
        # print(np.mean(ancienneImage[:,:,2]) - np.mean(image2[:,:,2]))

        # print(np.mean(ancienneImage[:,:,0]), np.mean(image[:,:,0]), np.mean(image2[:,:,0]), np.mean(image3[:,:,0]))
        # print(np.mean(ancienneImage[:,:,1]), np.mean(image[:,:,1]), np.mean(image2[:,:,1]), np.mean(image3[:,:,1]))
        # print(np.mean(ancienneImage[:,:,2]), np.mean(image[:,:,2]), np.mean(image2[:,:,2]), np.mean(image3[:,:,2]))
    # plt.imshow(image)
    # plt.show()
    # plt.imshow(ancienneImage)
    # plt.show()


if __name__ == "__main__":
    test_representation_image_complexe()
