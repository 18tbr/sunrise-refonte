import numpy as np
from random import randint
from scipy.integrate import solve_ivp   # Cersion moderne et orienté objet de odeint
import GrilleUtils


class Grille(object):
    """docstring for Grille."""

    def __init__(self, cint, T, Text, Tint, Pint):
        super(Grille, self).__init__()
        # La racine de l'arbre
        self.racine = None
        # Capacité thermique associée à l'air intérieur
        self.cint = cint
        # Nombre de condenasateurs dans le réseau, il doit au moins y avoir cint
        self.nbCondensateurs = 1
        # La forme du réseau, résumée au nombre de noeuds à chaque profondeur
        self.forme = []
        # La liste des temps (pour Text, Tint, Pint)
        self.T = T
        # La série des températures extérieures
        self.Text = Text
        # La série des températures intérieures
        self.Tint = Tint
        # La série des puissances intérieures
        self.Pint = Pint

    def creationSimulation(self):
        nbTemperatures = self.nbCondensateurs
        # L'équation différentielle à résoudre sera :
        # C^-1 dT/dt = AT + BQ
        # Pour la signification de chacune de ces matrices, voire les fonctions de résolution de l'équation différentielle.
        A = np.zeros((nbTemperatures, nbTemperatures))
        B = np.zeros((nbTemperatures,2))
        C = np.eye(nbTemperatures)
        C[0,0] /= self.cint  # La capacité sur Tint n'est pas dans l'arbre
        result, curseur = self.racine.creationSimulationRecursive(
            A, B, C, None, 0, 0
        )
        # Il reste à rentrer dans le tableau la valeur du lien entre Tint et Text
        if result is not None:
            B[0, 0] = result
            B[0, 1] = 1 # La puissance intérieure s'applique sur Tint
        # On crée récursivement le tableau en partant de la racine.
        return A, B, C

    def simulation(self):
        A, B, C = self.creationSimulation()
        # Résoudre C^-1 dT/dt = AT + BQ
        nbTemperatures = self.nbCondensateurs
        # Hypothèse : Au début de la simulation, tout est à l'équilibre à la température extérieure Text[0]
        T0 = np.full((nbTemperatures),self.Text[0])

        def gradient(T, t):
            # dT/dt = gradient(T,t) = C * (AT + BQ)
            return C @ (A @ T + B @ np.array([[self.Text[t]], [self.Pint[t]]]))

        return solve_ivp(gradient, self.T, T0, method='RK45', t_eval=self.T, vectorized=True)

    def score(self):
        # On calcule toutes le températures internes au fil du temps
        calcul = self.simulation()
        # On récupère la température intérieure (la première dans la matrice)
        calculTint = np.array([vecteur[0] for vecteur in calcul.y])
        # On calcule l'écart entre la température calculée et la référence
        ecart = self.Tint - calculTint
        # On renvoie l'écart quadratique cumulé
        return np.sum(np.square(ecart),0)


    def toImage(self, dimImage=(100, 100)):
        """
        Convertit un arbre en image.

        Parameters
        ----------
        dimImage : (int, int)
            Taille de l'image souhaitée (hauteur, largeur).
        """

        # création du canal représentant les résistances
        canalResistance = np.zeros(dimImage)
        GrilleUtils.creerCanalResistance(racine=self.racine,
                                         numRacine=0,
                                         NW=(0, 0),
                                         SE=dimImage,
                                         profondeur=0,
                                         image=canalResistance)
        # création du canal représentant les capacités
        canalCapacite = np.zeros(dimImage)
        GrilleUtils.creerCanalCapacite(racine=self.racine,
                                       numRacine=0,
                                       NW=(0, 0),
                                       SE=dimImage,
                                       profondeur=0,
                                       image=canalCapacite)
        # création du 3e canal ? Facultatif
        return None

    def fromImage(self, image):
        """
        Convertit une image en arbre, renvoie l'arbre.

        Parameters
        ----------
        image : numpy array
            Image à partir de laquelle créer un arbre.
        """
        return None


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

    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
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

    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
        listeTemperatures = [gauche]
        for i in range(len(self.capacites)):
            curseur += 1
            listeTemperatures.append(curseur)
        listeTemperatures.append(droite)

        for i in range(len(self.fils)):
            gaucheBranche = listeTemperatures[i]
            droiteBranche = listeTemperatures[i + 1]
            result, curseur = self.fils[i].creationSimulationRecursive(
                A, B, C, gaucheBranche, droiteBranche, curseur
            )
            if result is not None:
                # Text (i.e. gauche is None) a un traitement différent
                if gauche is None:
                    B[droiteBranche, 0] = result
                else:
                    # Termes hors diagonale
                    A[gaucheBranche, droiteBranche] = -result
                    A[droiteBranche, gaucheBranche] = -result
                    # Termes diagonaux
                    A[droiteBranche, droiteBranche] = result
                    A[gaucheBranche, gaucheBranche] = result
            if i + 1 < len(self.fils):
                C[droiteBranche, droiteBranche] /= self.capacites[i]
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

    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
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
