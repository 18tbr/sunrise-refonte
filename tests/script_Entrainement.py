import matplotlib.pyplot as plt
import os
import sys
import numpy as np

from random import randrange
from keras.models import load_model

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

import Coefficients
from Genetique import Genetique
from Entrainement import (
    lectureBlob,
    unificationPopulation,
)
from Autoencodeur import Autoencodeur


def test_entrainement():
    Genetique.PROFONDEUR_MAX_ARBRE = 20
    Genetique.LARGEUR_MAX_ARBRE = 20
    taille = 1
    l, h = 32, 32
    Cint = Coefficients.muC
    listeGenetiques = lectureBlob(
        Cint, taillePopulation=taille, generationMax=100, objectif=10
    )
    print(len(listeGenetiques))
    population = unificationPopulation(listeGenetiques)
    taille = len(population)
    print(taille)
    # scores = []
    images = []
    for i in range(len(population)):
        print(f"{i}/{taille}")
        # scores.append(-population[i].score())
        images.append(population[i].ecritureImage(largeur=l, hauteur=h))
    # plt.plot(range(taille), np.log(np.array(scores)))
    # plt.show()
    print("Creation de l'autoencodeur")
    # La liste des images sur lesquelles on va faire des tests à la fin
    test = []
    for i in range(5):
        index = randrange(len(images))
        test.append((images[index], population[index]))
        # del images[index]
    # Le réseau progresse en général beaucoup moins vite au dela de 50
    # itérations

    # testeur = Autoencodeur(largeur=l, hauteur=h, nomDuModele=None)
    # testeur.creationNouveau(baseNoyau=[9,7,5,3], baseDimensions=7, baseDense=50)
    # testeur.entrainementImitation(
    #     images, iterations=50, tailleGroupeEntrainement=8
    # )

    testeur = Autoencodeur(largeur=l, hauteur=h, nomDuModele="test")
    resultats = testeur.predire([elt[0] for elt in test])
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
