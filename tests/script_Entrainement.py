import matplotlib.pyplot as plt
import os
import sys
import numpy as np

from random import randrange

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

import Coefficients
from Genetique import Genetique
from Entrainement import lectureBlob, unificationPopulation

# On importe l'autoencodeur de test pour expérimenter
from script_aide_Autoencodeur import Autoencodeur

def test_entrainement():
    Genetique.PROFONDEUR_MAX_ARBRE = 20
    Genetique.LARGEUR_MAX_ARBRE = 20
    taille = 100
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
        images.append(population[i].ecritureImage(largeur=100, hauteur=100))
    # plt.plot(range(taille), np.log(np.array(scores)))
    # plt.show()
    print("Creation de l'autoencodeur")
    # La liste des images sur lesquelles on va faire des tests à la fin
    test = []
    for i in range(5):
        index = randrange(len(images))
        test.append(images[index])
        del images[index]
    testeur = Autoencodeur()
    testeur.entrainer(images)
    resultats = testeur.predire(test)
    for i in range(5):
        plt.imshow(test[i])
        plt.show()
        plt.imshow(resultats[i])
        plt.show()

if __name__ == "__main__":
    test_entrainement()
