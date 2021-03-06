"""Tests sur l'algorithme gééntique."""

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from random import choices

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

import intelligenceArtificielle.structureDonnees.Coefficients as Coefficients
from intelligenceArtificielle.Genetique import Genetique
from intelligenceArtificielle.Outils import (
    lireDossier,
)  # Pour récupérer des valeurs crédibles sur lesquelles lancer l'algorithme.


def test_population_aleatoire():
    taille = 20
    Cint = Coefficients.muC
    T, Tint, Text, Pint = lireDossier(
        os.path.join("blob", "mesures", "mesure4")
    )
    # T = list(range(taille))
    # Text = list(range(taille))
    # Tint = [10 * i for i in range(taille)]
    # Pint = [0 for i in range(taille)]
    Genetique.PROFONDEUR_MAX_ARBRE = 10
    Genetique.LARGEUR_MAX_ARBRE = 10
    Genetique.SILENCE = True
    # Genetique.ELAGUAGE_FORCE = False
    # choixAutoencodeur = None
    choixAutoencodeur = "base"
    print("Création de la population initiale")
    evolution = Genetique(
        Cint,
        T,
        Text,
        Tint,
        Pint,
        generationMax=30,
        imageLargeur=32,
        imageHauteur=32,
        autoencodeur=choixAutoencodeur,
    )
    # print("\nCalcul du score de tous les individus de la population")
    # listeScores = evolution.scorePopulation()
    # plt.plot(range(evolution.taillePopulation), [elt[1] for elt in listeScores])
    # plt.title("Répartition de score dans la population initiale")
    # plt.show()
    # lot = listeScores[::10] + listeScores[-2:]
    # for individu, score in lot:
    #     score = individu.score()
    #     image = individu.ecritureImage(largeur=100, hauteur=100)
    #     R, V, B = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    #     plt.imshow(image)
    #     plt.title(f"Image RVB d'un arbre de la population\nscore {score}")
    #     plt.show()
    #     plt.imshow(R, cmap="jet", vmin=0, vmax=255)
    #     plt.title(f"Image des résistances de l'arbre seules\nscore {score}")
    #     plt.colorbar()
    #     plt.show()
    #     plt.imshow(V, cmap="jet", vmin=0, vmax=255)
    #     plt.title(f"Image des condensateurs de l'arbre seuls\nscore {score}")
    #     plt.colorbar()
    #     plt.show()
    #     plt.imshow(B, cmap="jet", vmin=0, vmax=255)
    #     plt.title(
    #         f"Image de l'erreur propagée dans l'arbre seule\nscore {score}"
    #     )
    #     plt.colorbar()
    #     plt.show()

    Genetique.CHANCE_DE_MUTATION = 0.3
    optimiseur = evolution.optimisation()
    listeScores = []
    while True:
        try:
            generation, meilleurIndividu, meilleurScore = next(optimiseur)
            listeScores.append(meilleurScore)
            print(f"Génération {generation} - score {meilleurScore}.")
            # image = meilleurIndividu.ecritureImage(largeur=32, hauteur=32)
            # plt.imshow(image)
            # plt.title(f"Image RVB du meilleur arbre de la population")
            # plt.show()
        except StopIteration:
            break
    plt.plot(range(len(listeScores)), listeScores)
    if evolution.autoencodeur is None:
        plt.title(
            "Convergence de l'algorithme génétique seul (sans auto-encodeurs)"
        )
    else:
        plt.title(
            f"Convergence de l'algorithme génétique avec l'auto-encodeur {choixAutoencodeur}"
        )
    plt.show()


if __name__ == "__main__":
    test_population_aleatoire()
