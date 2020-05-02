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

def creation_simulation_recursive(noeud, tableau_simulation, gauche, droite, curseur):
    # Il faut aussi mettre à jour le curseur pour éviter d'écrire deux fois la même température.
    if type(noeud) == Parallele:
        return resolution_simulation_parallele(noeud, tableau_simulation, droite, gauche, curseur)
    elif type(noeud) == Serie:
        return resolution_simulation_serie(noeud, tableau_simulation, droite, gauche, curseur)
    elif type(noeud) == Feuille:
        return resolution_simulation_feuille(noeud, tableau_simulation, droite, gauche, curseur)


def creation_simulation(grille):
    nbTemperatures = grille.nbCondensateurs + 1
    tableau = np.zeroes((nbTemperatures, nbTemperatures))
    tableau[0, 0] = 0   # Pas de capacité sur Text
    tableau[nbTemperatures - 1, nbTemperatures - 1] = grille.Cint   # La capacité sur Tint n'est pas dans l'arbre
    result, curseur creation_simulation_recursive(grille.racine, tableau, 0, nbTemperatures - 1, 0)
    # Il reste à rentrer dans le tableau la valeur du lien entre Tint et Text
    if result is not None:
        tableau[0, nbTemperatures - 1] = result
        tableau[nbTemperatures - 1, 0] = result
    # On crée récursivement le tableau en partant de la racine.
    return tableau

def resolution_simulation_parallele(noeud, tableau_simulation, gauche, droite, curseur):
    result = 0
    for fils in noeud.fils:
        resultBranche, curseur = creation_simulation_recursive(fils, tableau_simulation, gauche, droite, curseur)
        if resultBranche is not None:
            result += resultBranche
    return result, curseur

def resolution_simulation_serie(noeud, tableau_simulation, gauche, droite, curseur):
    listeTemperatures = [gauche]
    for i in range(len(noeud.capacites)):
        curseur += 1
        listeTemperatures.append(curseur)
    listeTemperatures.append(droite)

    for i in range(len(noeud.fils)):
        gaucheBranche = listeTemperatures[i]
        droiteBranche = listeTemperatures[i+1]
        result, curseur = resolution_simulation_recursive(noeud.fils[i], tableau_simulation, gaucheBranche, droiteBranche, curseur)
        if result is not None:
            tableau_simulation[gaucheBranche, droiteBranche] = result
            tableau_simulation[droiteBranche, gaucheBranche] = result
        if i + 1 < len(noeud.fils):
            tableau_simulation[droiteBranche, droiteBranche] = noeud.capacites[i]
    return None, curseur


def resolution_simulation_feuille(noeud, tableau_simulation, gauche, droite, curseur):
    return noeud.H, curseur
