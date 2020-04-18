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

    def creer_maille():
        # Crée la maille qui servira de support au calcul. Il s'agit juste de créer la liste des Noeuds. Les paramètres utiles pour les propriétés des noeuds seront fournis plus tard.
        pass

    def creer_murs():
        # Mets à jour les noeuds qui font partie des murs de la maison en utilisant les paramètres fournis.
        pass


class Noeud(object):
    """docstring for Noeud."""

    def __init__(self, coordonnees, grille, proprietes = {}):
        super(Noeud, self).__init__()
        # Un triplet i,j,k donnant les coordonnées du noeud dans la maille.
        self.coord = coordonnees
        # Il faut assigner à un attribut du Noeud chacun de ses propriétés, par exemple si on a dans le dictionnaire proprietes une proprietée rho (pour la masse volumique) il faut créer un champs rho dans le noeud qui contienne la valeur de la masse volumique. Les champs à définir seront choisis à l'avance.

        # La grille dont ce noeud fait partie, utile pour trouver les voisins etc...
        self.grille = grille

    def mettre_a_jour(proprietes):
        # Met à jour les champs du noeud avec les valeurs dans le dictionnaire proprietes
        pass

    def voisins(self):
        # Renvoie la liste des voisins du noeud dans la maille
        return []
