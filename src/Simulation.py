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
