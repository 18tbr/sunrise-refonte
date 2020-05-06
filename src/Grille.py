import numpy as np
from random import randint


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

    def creationSimulation(self):
        nbTemperatures = self.nbCondensateurs + 1
        tableau = np.zeros((nbTemperatures, nbTemperatures))
        tableau[0, 0] = 0  # Pas de capacité sur Text
        tableau[
            nbTemperatures - 1, nbTemperatures - 1
        ] = self.cint  # La capacité sur Tint n'est pas dans l'arbre
        result, curseur = self.racine.creationSimulationRecursive(
            tableau, 0, nbTemperatures - 1, 0
        )
        # Il reste à rentrer dans le tableau la valeur du lien entre Tint et Text
        if result is not None:
            tableau[0, nbTemperatures - 1] = result
            tableau[nbTemperatures - 1, 0] = result
        # On crée récursivement le tableau en partant de la racine.
        return tableau

    def to_image(self, img_size=(100, 100)):
        """
        Convertit un arbre en image.

        Parameters
        ----------
        img_size : (int, int)
            Taille de l'image souhaitée (hauteur, largeur).
        """

        def image_fill(image, NW, SE, val):
            """
            Colorie une zone de l'image.

            Parameters
            ----------
            image : numpy array
                Image to fill.
            NW = (NW_h, NW_w) : (int, int)
                North-West corner of portion of image.
            SE = (SE_h, SE_w) : (int, int)
                South-East corner of portion of image.
            val : int
                Value to affect to portion of image.
            """
            print(f"On colorie de {NW} à {SE}")
            NW_h, NW_w = NW
            SE_h, SE_w = SE
            image[NW_h:SE_h, NW_w:SE_w] = val

        def make_resistance_channel(image, racine, num_racine, NW, SE, profondeur):
            """
            Fonction récursive de création du channel résistance de l'arbre.

            Parameters
            ----------
            image : numpy array
                Image to modify.
            racine : Noeud
            num_racine : int
                Numéro de la racine parmi les fils de son père.
            NW = (NW_h, NW_w) : (int, int)
                North-West corner of portion of image.
            SE = (SE_h, SE_w) : (int, int)
                South-East corner of portion of image.
            profondeur : int
                profondeur de racine, utile pour savoir si l'on divise
                verticalement ou horizontalement.
                On alterne le sens de division, et on commence par une
                division verticale.

            """
            # get coord
            NW_h, NW_w = NW
            SE_h, SE_w = SE
            # cas de base
            if type(racine) is Feuille:
                print(f"Feuille de valeur {racine.val}")
                image_fill(image, NW, SE, racine.val)
            # else...
            else:
                print(f"Noeud")
                for num_fils, fils in enumerate(racine.fils):
                    total_fils = len(racine.fils)
                    if type(racine) is Serie:  # on divise verticalement
                        # upper left
                        new_NW_h = NW_h
                        new_NW_w = NW_w + (SE_w - NW_w) * num_fils // total_fils
                        # down right
                        new_SE_h = SE_h
                        new_SE_w = NW_w + (SE_w - NW_w) * (num_fils + 1) // total_fils
                    else:  # on divise horizontalement
                        # upper left
                        new_NW_h = NW_h + (SE_h - NW_h) * num_fils // total_fils
                        new_NW_w = NW_w
                        # down right
                        new_SE_w = SE_w
                        new_SE_h = NW_h + (SE_h - NW_h) * (num_fils + 1) // total_fils
                    new_NW = (new_NW_h, new_NW_w)
                    new_SE = (new_SE_h, new_SE_w)
                    # appel résursif
                    make_resistance_channel(image, fils, num_fils, new_NW, new_SE, profondeur + 1)

        image = np.zeros(img_size)
        make_resistance_channel(racine=self.racine,
                                num_racine=0,
                                NW=(0, 0),
                                SE=img_size,
                                profondeur=0,
                                image=image)

        return image



class Noeud(object):
    """docstring for Noeud."""

    def __init__(self):
        super(Noeud, self).__init__()
        self.fils = []

    # Méthode abstraite, on supprime le fils à l'index i
    # Notez que comme ajoutFils peut changer la natuer d'un fils, le pattern pour l'utiliser est quelque chose comme :
    # noeudChoisi.fils[i] = noeudChoisi.fils[i].suppressionFils(index)
    # C'est à dire que le noeud n'est pas modifié en place, ce qui est assez frustrant. Pour le modifier en place il faudrait utiliser un pattrn différent, je vous laisse en trouver un qui marche.
    # Une façon de faire cela serait d'avoir une référence au parent dans chaque noeud.
    def suppressionFils(self, index):
        raise NotImplementedError("La supppression d'un fils n'a pas été réimplémenté.")

    # Méthode abstraite, contraire de suppressionFils
    # Notez que comme ajoutFils peut changer la natuer d'un fils, le pattern pour l'utiliser est quelque chose comme :
    # noeudChoisi.fils[i] = noeudChoisi.fils[i].ajoutFils(fils, index)
    # C'est à dire que le noeud n'est pas modifié en place, ce qui est assez frustrant. Pour le modifier en place il faudrait utiliser un pattrn différent, je vous laisse en trouver un qui marche.
    def ajoutFils(self, nouveauFils, index, forme=None):
        raise NotImplementedError("L'ajout d'un fils n'a pas été implémenté.")


class Parallele(Noeud):
    """docstring for Parallele."""

    def __init__(self, arg):
        super(Parallele, self).__init__()
        pass

    def creationSimulationRecursive(self, tableau, gauche, droite, curseur):
        result = 0
        for fils in self.fils:
            resultBranche, curseur = fils.creationSimulationRecursive(
                tableau, gauche, droite, curseur
            )
            if resultBranche is not None:
                result += resultBranche
        return result, curseur

    def suppressionFils(self, index):
        # Renvoie le noeud qui doit remplacer celui-ci une fois la suppression effectuée.
        # IndexError out of range si index est trop grand pour self.fils
        del self.fils[index]
        taille = len(self.fils)
        if taille > 2:
            # S'il reste des blocs en parallèle on renvoie tous les blocs en parallèle.
            return self
        else:
            # S'il ne reste plsu qu'un seul bloc il prend la place du bloc parallèle
            return self.fils[0]


    def ajoutFils(self, nouveauFils, index, forme=None):
        if forme is not None:
            raise NonFeuilleException("Vous ne pouvez pas changer le forme d'un noeud (non feuille) qui existe déjà avec ajoutFils !")
        elif index is None:
            raise NonFeuilleException("Vous devez préciser à quel index insérer le nouveau fils parmi les fils du noeud préexistant !")
        if index == len(self.fils):
            self.fils.append(nouveauFils)
        else:
            self.fils.insert(index, nouveauFils)
        # On remplace le noeud par lequel on doit remplacer l'ancien pour que l'ajout compte bien.
        return self


class Serie(Noeud):
    """docstring for Serie."""

    def __init__(self):
        super(Serie, self).__init__()
        self.capacites = []
        self.valeurCapaciteDefaut = 1

    def creationSimulationRecursive(self, tableau, gauche, droite, curseur):
        listeTemperatures = [gauche]
        for i in range(len(self.capacites)):
            curseur += 1
            listeTemperatures.append(curseur)
        listeTemperatures.append(droite)

        for i in range(len(self.fils)):
            gaucheBranche = listeTemperatures[i]
            droiteBranche = listeTemperatures[i + 1]
            result, curseur = self.fils[i].creationSimulationRecursive(
                tableau, gaucheBranche, droiteBranche, curseur
            )
            if result is not None:
                tableau[gaucheBranche, droiteBranche] = result
                tableau[droiteBranche, gaucheBranche] = result
            if i + 1 < len(self.fils):
                tableau[droiteBranche, droiteBranche] = self.capacites[i]
        return None, curseur

    def suppressionFils(self, index):
        # Renvoie le noeud qui doit remplacer celui-ci une fois la suppression effectuée.
        # IndexError si index est trop grand pour self.fils
        del self.fils[index]
        taille = len(self.fils)
        # Pour une liaison série il faut également supprimer la capacité intermédiaire.
        if index == taille:
            # i.e. on a supprimé le dernier élément de l'ancienne liste des fils.
            del self.capacites[-1]
        else:
            del self.capacites[index]
        if taille >= 2:
            # S'il reste des blocs en parallèle on renvoie tous les blocs en parallèle.
            return self
        else:
            # S'il ne reste plsu qu'un seul bloc il prend la place du bloc parallèle
            return self.fils[0]

    def ajoutFils(self, nouveauFils, index=None, forme=None):
        if forme is not None:
            raise NonFeuilleException("Vous ne pouvez pas changer le forme d'un noeud (non feuille) qui existe déjà avec ajoutFils !")
        elif index is None:
            raise NonFeuilleException("Vous devez préciser à quel index insérer le nouveau fils parmi les fils du noeud préexistant !")
        taille = len(self.fils)
        # Il faut aussi aojuter une valeur de capacité intermédiaire dans le cas d'une liaison série.
        if index == taille or index == taille + 1:
            self.capacites.append(self.valeurCapaciteDefaut)
        else:
            self.capacites.insert(index, self.valeurCapaciteDefaut)
        self.fils.insert(index, nouveauFils)
        # On remplace le noeud par lequel on doit remplacer l'ancien pour que l'ajout compte bien.
        return self



class Feuille(Noeud):
    """docstring for Feuille."""

    def __init__(self):
        super(Feuille, self).__init__()
        self.H = 0
        self.val = randint(0, 42)

    def creationSimulationRecursive(self, tableau, gauche, droite, curseur):
        return self.H, curseur

    @property
    def fini(self):
        raise FeuilleException("Une feuille n'a pas de fils !")

    def suppressionFils(self, index):
        raise FeuilleException("Une feuille n'a pas de fils !")

    def ajoutFils(self, nouveauFils, index=None, forme=None):
        if forme is None or forme not in ['parallele', 'serie']:
            raise FeuilleException("Pour créer un nouveau noeud à partir d'une feuille il faut préciser la forme à donner, l'un de 'parallele' ou 'serie'.")
        elif index is not None:
            raise FeuilleException("Pour créer un nouveau noeud à partir d'une feuille il ne faut pas préciser d'index, qui n'est utilisable que pour un noeud Parallele ou Serie.")
        elif forme == 'parallele':
            nouveauNoeud = Parallele()
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
            return nouveauNoeud
        elif forme == 'serie':
            nouveauNoeud = Serie()
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
            return nouveauNoeud



# Une erreur est apparue car vous utilisé une syntaxe invalide sur une feuille.
class FeuilleException(Exception):
    # Syntaxe spéciale pour une déclaration d'exceptions plus rapide
    pass

# Une erreur est apparue car vous avez utilisé une syntaxe spécifique aux feuilles pour un noeud.
class NonFeuilleException(Exception):
    # Syntaxe spéciale pour une déclaration d'exceptions plus rapide
    pass
