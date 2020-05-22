# Ce fichiers contient plusieurs fonctions utiles pour rendre le code de l'interface graphique plus simple et lisible.

import os   # Utile pour les manipulations de noms de fichiers
import numpy as np  # Utile pour les manipulations de tableaux

def lireTableau(nomDuFichier):
    # Lit le tableau qui se trouve dans le fichier nomFichier et le renvoie sous la forme d'un np.array
    baseNom, extension = os.path.splitext(nomDuFichier)
    if extension == ".npy":
        return np.load(nomDuFichier)
    elif extension == ".csv":
        return np.loadtxt(nomDuFichier, dtype=float, delimiter=",")
    else:
        raise ValueError("Le fichier présenté ne ressemble à aucun type de fichiers connus.")
