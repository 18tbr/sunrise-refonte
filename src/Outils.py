"""Ce fichier contient plusieurs fonctions utiles pour rendre le code de
l'interface graphique plus simple et lisible."""

import os  # Utile pour les manipulations de noms de fichiers
import numpy as np  # Utile pour les manipulations de tableaux


def lireTableau(nomDuFichier):
    """Lit un tableau et le renvoie sous la forme d'un np.array.

    Paramètres
    ----------
    nomDuFichier : string
        Tableau à lire.

    Exceptions levées
    -----------------
    ValueError
        Lorsque le fichier `nomDuFichier` n'existe pas.
    """
    baseNom, extension = os.path.splitext(nomDuFichier)
    if extension == ".npy":
        return np.load(nomDuFichier)
    elif extension == ".csv":
        return np.loadtxt(nomDuFichier, dtype=float, delimiter=",")
    else:
        raise ValueError(
            "Le fichier présenté ne ressemble à aucun type de fichiers connus."
        )


def lireDossier(nomDuDossier):
    """Simplifie l'entrainement en récupérant directement toutes les grandeurs
    d'intérêt à partir des fichiers .csv contenus dans un dossier.

    Paramètres
    ----------
    nomDuDossier : str
        Dossier cible.

    Exceptions levées
    -----------------
    ValueError
        Lorsque les fichiers (Tint.csv, Text.csv et Pint.csv) attendus
        n'existent pas dans le dossier `nomDuDossier`.
    ValueError
        Lorsque les différentes grandeurs données n'ont pas la même base de
        temps, et ne peuvent donc pas être utilisées ensemble.
    """
    fichierTint = os.path.join(nomDuDossier, "Tint.csv")
    fichierText = os.path.join(nomDuDossier, "Text.csv")
    fichierPint = os.path.join(nomDuDossier, "Pint.csv")

    # On lit les différents fichiers trouvés et on les transpose pour plus de
    # facilité.
    tableauTint = lireTableau(fichierTint).T
    tableauText = lireTableau(fichierText).T
    tableauPint = lireTableau(fichierPint).T

    # On vérifie que les données ont toutes la même base de temps.
    tempsTint, Tint = tableauTint[0], tableauTint[1]
    tempsText, Text = tableauText[0], tableauText[1]
    tempsPint, Pint = tableauPint[0], tableauPint[1]

    if (tempsTint - tempsText).any() or (tempsPint - tempsText).any():
        raise ValueError(
            "Les différentes grandeurs données n'ont pas la même base de temps et ne peuvent donc pas être utilisées ensemble."
        )
    # si tout a fonctionné, on renvoie les tableaux d'intérêt
    return tempsTint, Tint, Text, Pint
