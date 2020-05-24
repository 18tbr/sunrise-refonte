# Ce fichier contient un ensemble de méthodes utiles à l'entrainement des autoencodeurs.

import numpy as np

import os  # Utile pour les manipulations de fichiers
from GenerateurArbres import GenerateurArbres
from Outils import lireTableau, lireDossier  # Utile pour récupérer les mesures


def creationPopulationLectureDossier(
    dossier, Cint, taillePopulation, largeur, hauteur
):
    # Renvoie une population créée à partir des mesures trouvées dans le dossier en argument. Notez que l'on n'élague pas la population créée si largeur ou hauteur est None.
    T, Tint, Text, Pint = lireDossier(dossier)
    if largeur is not None and hauteur is not None:
        elaguageForce = True
    else:
        elaguageForce = False

    return GenerateurArbres(
        Cint, T, Tint, Text, Pint, taillePopulation, largeur, hauteur, elaguageForce
    ).population


def lectureBlob(Cint, taillePopulation, largeur, hauteur):
    # Renvoie la concaténation des populations créées à partir des données dans les dossiers de blob. Cette fonction doit être lancée lorsque le répertoire courant est la racine de ce dépôt git.
    listeDossiers = os.listdir(os.path.join("blob", "mesures"))
    population = []
    for dossier in listeDossiers:
        print(
            "Récupération des mesures dans le dossier",
            os.path.join("blob", "mesures", dossier),
        )
        # On ajoute la population crée à partir du dossier dans notre population totale. Notez que si largeur ou hauteur est None, la population ne sera pas élaguée.
        population += creationPopulationLectureDossier(
                os.path.join("blob", "mesures", dossier),
                Cint,
                taillePopulation,
                largeur,
                hauteur
            )
    return population
