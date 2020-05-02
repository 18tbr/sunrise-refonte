import numpy as np

class Grille(object):
    """docstring for Grille."""

    def __init__(self, cint):
        super(Grille, self).__init__()
        # La racine de l'arbre
        self.racine = None
        # Capacité thermique associée à l'air intérieur
        self.cint = cint
        # Nombre de condenasateurs dans le réseau, il doit au moins y avoir cint
        self.nbCondensateurs = 1
        # La forme du réseau, résumée au nombre de noeuds à chaque profondeur
        self.forme = []

    def creation_simulation(self):
        nbTemperatures = self.nbCondensateurs + 1
        tableau = np.zeroes((nbTemperatures, nbTemperatures))
        tableau[0, 0] = 0   # Pas de capacité sur Text
        tableau[nbTemperatures - 1, nbTemperatures - 1] = self.cint   # La capacité sur Tint n'est pas dans l'arbre
        result, curseur = self.racine.creation_simulation_recursive(tableau, 0, nbTemperatures - 1, 0)
        # Il reste à rentrer dans le tableau la valeur du lien entre Tint et Text
        if result is not None:
            tableau[0, nbTemperatures - 1] = result
            tableau[nbTemperatures - 1, 0] = result
        # On crée récursivement le tableau en partant de la racine.
        return tableau


class Noeud(object):
    """docstring for Noeud."""

    def __init__(self):
        super(Noeud, self).__init__()
        self.fils = []


class Parallele(Noeud):
    """docstring for Parallele."""

    def __init__(self, arg):
        super(Parallele, self).__init__()
        pass

    def creation_simulation_recursive(self, tableau, gauche, droite, curseur):
        result = 0
        for fils in self.fils:
            resultBranche, curseur = fils.creation_simulation_recursive(tableau_simulation, gauche, droite, curseur)
            if resultBranche is not None:
                result += resultBranche
        return result, curseur


class Serie(Noeud):
    """docstring for Serie."""

    def __init__(self):
        super(Serie, self).__init__()
        self.capacites = []

    def creation_simulation_recursive(self, tableau, gauche, droite, curseur):
        listeTemperatures = [gauche]
        for i in range(len(self..capacites)):
            curseur += 1
            listeTemperatures.append(curseur)
        listeTemperatures.append(droite)

        for i in range(len(self..fils)):
            gaucheBranche = listeTemperatures[i]
            droiteBranche = listeTemperatures[i+1]
            result, curseur = self.fils[i].resolution_simulation_recursive(tableau_simulation, gaucheBranche, droiteBranche, curseur)
            if result is not None:
                tableau_simulation[gaucheBranche, droiteBranche] = result
                tableau_simulation[droiteBranche, gaucheBranche] = result
            if i + 1 < len(self.fils):
                tableau_simulation[droiteBranche, droiteBranche] = self.capacites[i]
        return None, curseur

class Feuille(Noeud):
    """docstring for Feuille."""

    def __init__(self):
        super(Feuille, self).__init__()
        self.H = 0

    def creation_simulation_recursive(self, tableau, gauche, droite, curseur):
        return self.H, curseur
