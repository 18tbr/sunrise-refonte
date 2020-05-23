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
from Entrainement import lectureBlob, unificationPopulation, CreateurAutoencodeur

def test_entrainement():
    Genetique.PROFONDEUR_MAX_ARBRE = 20
    Genetique.LARGEUR_MAX_ARBRE = 20
    taille = 5
    l, h = 32, 32
    Cint = Coefficients.muC
    listeGenetiques = lectureBlob(Cint, taillePopulation=taille, generationMax=100, objectif=10)
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
        test.append(images[index])
        del images[index]
    # Le réseau progresse en général beaucoup moins vite au dela de 50
    # itérations
    testeur = CreateurAutoencodeur(largeur=l, hauteur=h)
    testeur.entrainer(images, iterations=10, tailleGroupeEntrainement=8)
    # resultats = testeur.predire(test)
    # for i in range(5):
    #     plt.imshow(test[i])
    #     plt.show()
    #     plt.imshow(resultats[i])
    #     plt.show()
    testeur.sauver("blob/model.md5")
    testChargement = load_model("blob/model.md5")
    testChargement.summary()
    print("Chargement réussi.")


if __name__ == "__main__":
    test_entrainement()
