"""
commentaire
"""

import sklearn
import joblib

class AI(object):
    """docstring for AI."""

    def __init__(self, args, parametres, sorties, experience):
        super(AI, self).__init__()
        # Les arguments de l'experience
        self.args = args
        # Les sorties récupérées de la simulation
        self.sorties = sorties
        # Les résultats récupérés par l'expérience
        self.experience = experience
        # Le modèle d'intelligence artificiel préentrainé
        self.model = None
        # La prévision obtenue par le modèle d'intelligence artificielle
        self.prevision = {}

    def lecture_modele():
        # Récupère le modèle entrainé depuis le fichier modele.skl et le met dans self.model
        pass


    def sauvegarde_modele():
        # Récupère le modèle entrainé dans self.model et le sauvegarde dans le fichier modele.skl
        pass
