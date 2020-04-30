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

def creation_simulation_recursive(noeud,tableau_simulation,droite,gauche):
    if noeud. == "parallele":
        resolution_simulation_parallele(noeud,tableau_simulation,droite,gauche)
    if noeud == "serie":
        resolution_simulation_serie(noeud,tableau_simulation,droite,gauche)

def creation_simulation(grille):
    nbTemperatures = grille.nbCondensateurs + 1
    tableau = np.zeroes((nbTemperatures, nbTemperatures))
    tableau[0, 0] = 0   # Pas de capacité sur Text
    tableau[nbTemperatures - 1, nbTemperatures - 1] = grille.Cint   # La capacité sur Tint n'est pas dans l'arbre
    creation_simulation_recursive(grille.racine, tableau, 0, nbTemperatures - 1)
    # On crée récursivement le tableau en partant de la racine.
    return tableau

def resolution_simulation_parallele(noeud, tableau_simulation, droite, gauche):
    pass

def resolution_simulation_serie(noeud, tableau_simulation, droite, gauche):
    pass

def resolution_simulation_feuille(noeud, tableau_simulation, droite, gauche):
    pass
