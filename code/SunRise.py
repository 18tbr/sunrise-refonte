import numpy as np

class SunRise(object):
    """docstring for SunRise."""

    def __init__(self, parametresUI):
        super(SunRise, self).__init__()
        # Les paramètres entrés par l'utilisateur dans l'interface
        self.pUI = parametresUI
        # Un dictionnaire contenant tous les arguments de la simulation, utiles pour le groupe Simulation
        self.args = {}
        # Un dictionnaire contenant tous les paramètres de la simulation, utile pour le groupe Grille
        self.parametres = {}
