import tkinter as tk
from Animation import *

class UI(object):
    """docstring for UI."""

    def __init__(self):
        super(UI, self).__init__()
        # Un dictionnaire contenant toutes les valeurs rentrées par l'utilisateur dans l'interface et qui pourront seront utilisées pour la simulation
        self.pUI = {}
        # L'objet Animation que l'on voudra afficher.
        self.animation = None


    def lecture_parametres():
        # Fonction responsable de lire les paramètres précédemment utilisés par l'application depuis le fichier parametres_ui.json et de les mettre dans self.pUI
        pass


    def sauvegarde_parametres():
        # Sauvegarde les valeurs de self.pUI dans le fichier parametres_ui.json.
        pass
