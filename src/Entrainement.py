# Ce fichier contient un ensemble de méthodes utiles à l'entrainement des autoencodeurs.

import numpy as np

import os  # Utile pour les manipulations de fichiers
from Genetique import Genetique
from Outils import lireTableau, lireDossier  # Utile pour récupérer les mesures


def creationGenetiqueLectureDossier(
    dossier, Cint, taillePopulation, generationMax, objectif
):
    # Renvoie un objet génétique crée à partir des mesures trouvées dans le dossier en argument.
    T, Tint, Text, Pint = lireDossier(dossier)
    return Genetique(
        Cint, T, Tint, Text, Pint, taillePopulation, generationMax, objectif
    )


def lectureBlob(Cint, taillePopulation, generationMax=None, objectif=None):
    # Renvoie la liste des population crées à partir des données dans les dossiers de blob. Cette fonction doit être lancée lorsque le repértoire courant est la racine de ce dépôt git.
    listeDossiers = os.listdir(os.path.join("blob", "mesures"))
    populations = []
    for dossier in listeDossiers:
        print(
            "Récupération des mesures dans le dossier",
            os.path.join("blob", "mesures", dossier),
        )
        # Dans la mesure où les Genetique produits ne sont utilisés que pour produire des arbres aléatoires, on peut ne pas leur fournir certains paramètres
        populations.append(
            creationGenetiqueLectureDossier(
                os.path.join("blob", "mesures", dossier),
                Cint,
                taillePopulation,
                generationMax,
                objectif,
            )
        )
    return populations


def unificationPopulation(listeGenetiques):
    # Prend en argument une liste d'objets Génétique et renvoie le liste de toutes leurs populations concaténées. Utile pour avoir une seule liste pour l'entrainement d'un autoencodeurs.
    populationUnifie = []
    for objetGenetique in listeGenetiques:
        populationUnifie += objetGenetique.population
    return populationUnifie
