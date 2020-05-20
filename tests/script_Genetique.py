import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from random import choices

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

import Coefficients
from Genetique import Genetique


def test_population_aleatoire():
    len = 30
    Cint = Coefficients.muC
    T = list(range(len))
    Text = list(range(len))
    Tint = [10 * i for i in range(len)]
    Pint = [0 for i in range(len)]
    Genetique.PROFONDEUR_MAX_ARBRE = 50
    Genetique.LARGEUR_MAX_ARBRE = 50
    print("Création de la population initiale")
    evolution = Genetique(Cint, T, Text, Tint, Pint)
    print("\nCalcul du score de tous les individus de la population")
    listeScores = evolution.scorePopulation()
    plt.plot(range(evolution.taillePopulation), [elt[1] for elt in listeScores])
    plt.title("Répartition de score dans la population initiale")
    plt.show()
    lot = listeScores[::10] + listeScores[-2:]
    for individu, score in lot:
        score = individu.score()
        image = individu.ecritureImage(largeur=100, hauteur=100)
        R, V, B = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        plt.imshow(image)
        plt.title(f"Image RVB d'un arbre de la population\nscore {score}")
        plt.show()
        plt.imshow(R, cmap="jet", vmin=0, vmax=255)
        plt.title(f"Image des résistances de l'arbre seules\nscore {score}")
        plt.colorbar()
        plt.show()
        plt.imshow(V, cmap="jet", vmin=0, vmax=255)
        plt.title(f"Image des condensateurs de l'arbre seuls\nscore {score}")
        plt.colorbar()
        plt.show()
        plt.imshow(B, cmap="jet", vmin=0, vmax=255)
        plt.title(
            f"Image de l'erreur propagée dans l'arbre seule\nscore {score}"
        )
        plt.colorbar()
        plt.show()


if __name__ == "__main__":
    test_population_aleatoire()
