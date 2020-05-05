import numpy as np
from scipy.integrate import odeint


class Simulation(object):
    """docstring for Simulation."""

    def __init__(self, grille, args):
        super(Simulation, self).__init__()
        # Contient les arguments de la simulation
        self.args = args
        # Contient la grille qui sert de support à la simulation
        self.grille = grille
        # Continent la sortie de la simulation
        self.sortie = {}
        # Indique si la simulation a fini de tourner ou non
        self.fini = False

def creation_simulation(grille, tableau_simulation):
    pass

def creation_recursive(noeud, tableau_simulation, droite, gauche):
    pass

def resolution_simulation_parallele(noeud, tableau_simulation, droite, gauche):
    pass

def resoultion_simulation_serie(noeud, tableau_simulation, droite, gauche):
    pass

# (Litao) Selons moi, cette fonction ne sert qu'à renvoyer les chiffres des résistances
# pour faire les calculs 
def resoultion_simulation_feuille(noeud, tableau_simulation, droite, gauche): 
    return noeud.arg


