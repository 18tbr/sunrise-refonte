#!/usr/bin/env python3

import os  # Utile pour les manipulations de chemins
import sys  # Utile pour modifier le dossier courant et le PYTHONPATH


def lancement_interface_graphique():
    """
    Cette fonction sert à lancer proprement l'interface graphique du projet SunRise refonte.
    """

    # Le chemin d'où l'utilisateur a lancé le programme
    cheminUtilisateur = os.getcwd()
    # On essaie de trouver le chemin de ce fichier, qui devrait toujours fonctionner sauf si ce code est lancé par un autre script python avec le même interpréteur.
    cheminSunRise = os.path.abspath(os.path.dirname(__file__))
    # On se place dans le dossier où se trouve ce script
    os.chdir(cheminSunRise)
    # Petite vérification, on vérifie que le présent script se trouve bien dans le dossier.
    if not os.path.exists("sunrise.py"):
        raise FileNotFoundError(
            "Le script n'est pas parvenu à trouver la racine du module sunrise-refonte et ne peut donc pas lancer l'interface graphique."
        )
    # Sinon, on ajoute src au PYTHONPATH
    sys.path.append(f"{cheminSunRise}/src")
    # On importe l'interface graphique
    from InterfaceGraphique import InterfaceGraphique

    # On créé l'interface graphique dans le dossier demandé
    interface = InterfaceGraphique(cheminUtilisateur)
    # Et enfin, on lance l'interface graphique pour l'utilisateur
    interface.afficher()


if __name__ == "__main__":
    lancement_interface_graphique()
