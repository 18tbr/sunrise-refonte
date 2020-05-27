import matplotlib.pyplot as plt
import os
import sys
import numpy as np

from random import randrange
from keras.models import load_model

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

import intelligenceArtificielle.structureDonnees.Coefficients as Coefficients
from intelligenceArtificielle.Genetique import Genetique
from intelligenceArtificielle.Entrainement import (
    creationPopulationLectureDossier,
    lectureBlob,
)
from intelligenceArtificielle.Autoencodeur import Autoencodeur
from intelligenceArtificielle.AutoencodeurDeterministe import (
    AutoencodeurDeterministe,
)


def test_entrainement():
    Genetique.PROFONDEUR_MAX_ARBRE = 6
    Genetique.LARGEUR_MAX_ARBRE = 4
    taille = 10
    l, h = 64, 64
    Cint = Coefficients.muC

    # On prend 5 arbres aléatoires pour faire nos tests
    populationTest = creationPopulationLectureDossier(
        os.path.join("blob", "mesures", "mesure4"),
        Cint,
        taillePopulation=l,
        largeur=l,
        hauteur=h,
    )[:5]

    # La liste des images sur lesquelles on va faire des tests à la fin
    test = []
    for arbre in populationTest:
        test.append((arbre.ecritureImage(largeur=l, hauteur=h), arbre))

    # ENTRAINEMENT
    # Le réseau progresse en général beaucoup moins vite au dela de 50
    # itérations en général
    testeur = AutoencodeurDeterministe(largeur=l, hauteur=h, nomDuModele=None)
    testeur.creation(baseNoyau=[9, 7, 5, 3], baseDimensions=7, baseDense=50)
    testeur.entrainementImitationBlob(
        Cint, taillePopulation=taille, iterations=50, tailleGroupeEntrainement=8
    )

    # # UTILISATION
    # testeur = AutoencodeurDeterministe(largeur=l, hauteur=h, nomDuModele="base")

    # TEST
    # On améliore nos arbres par effet de bord
    testeur.ameliorerArbres([elt[1] for elt in test])
    resultats = [
        arbre.ecritureImage(largeur=l, hauteur=h)
        for arbre in [elt[1] for elt in test]
    ]
    for i in range(5):
        imageReference, arbre = test[i]
        print(arbre.forme)
        plt.imshow(imageReference)
        plt.title("Reference")
        plt.show()
        plt.imshow(resultats[i])
        plt.title("Proposition brute")
        plt.show()
        imageNormalisee = arbre.normalisationImage(resultats[i])
        plt.imshow(imageNormalisee)
        plt.title("Proposition normalisée")
        plt.show()
    # testeur.sauver("test")
    # testChargement = load_model(os.path.join("src", "modeles", "test.md5"))
    # testChargement.summary()
    # print("Chargement réussi.")


if __name__ == "__main__":
    test_entrainement()
