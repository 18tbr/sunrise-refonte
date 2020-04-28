import numpy as np
import googlemaps

class Grille(object):
    """docstring for Grille."""

    def __init__(self, parametres):
        super(Grille, self).__init__()
        # Les parametres de la grille, récupérés du groupe SunRise
        self.parametres = parametres
        # Une liste contenant tous les noeuds utilisés pour la simulation
        self.noeuds = []


class Noeud(object):
    """docstring for Noeud."""

    def __init__(self, coordonnees, grille, proprietes = {}):
        super(Noeud, self).__init__()
        pass


class Parallele(object):
    """docstring for Parallele."""

    def __init__(self, arg):
        super(Parallele, self).__init__()
        self.arg = arg


class Serie(object):
    """docstring for Serie."""

    def __init__(self, arg):
        super(Serie, self).__init__()
        self.arg = arg


class Feuille(object):
    """docstring for Feuille."""

    def __init__(self, arg):
        super(Feuille, self).__init__()
        self.arg = arg
