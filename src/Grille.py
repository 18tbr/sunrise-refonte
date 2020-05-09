import numpy as np
from random import randint
from scipy.integrate import solve_ivp   # Version moderne et orienté objet de odeint
import GrilleUtils


class Grille(object):
    """docstring for Grille."""

    def __init__(self, cint, T, Text, Tint, Pint):
        super(Grille, self).__init__()
        # La racine de l'arbre
        self.racine = None
        # Capacité thermique associée à l'air intérieur
        self.cint = cint
        # Nombre de condensateurs dans le réseau, il doit au moins y avoir cint
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


    # Effectue un parcours en profondeur de l'arbre sous la racine jusqu'à atteindre le index ième noeud à la profondeur donnée. Renvoie le noeud trouvé.
    def inspecter(self, profondeur, index):
        if profondeur >= len(self.forme):
            raise IndexError(f"La profondeur de l'arbre désigné est {len(self.forme)}, il n'y a donc pas de noeuds à la profondeur {profondeur}.")
        # else...

        file = [self.racine]
        filePrecedente = [self.racine]
        profondeurParcours = 0
        while profondeurParcours < profondeur:
            file = []
            for noeudChoisi in filePrecedente:
                # Concatenation de liste
                file += noeudChoisi.fils
            profondeurParcours += 1
            filePrecedente = file

        if index >= len(file):
            raise IndexError(f"Il n'y a que {len(file)} noeuds à la profondeur {profondeur} de cette arbre, vous ne pouvez donc pas en récupérer le {index}ième.")
        # else...

        return file[index]

    def ecritureImage(self, dimImage=(100, 100, 3)):
        """
        Convertit un arbre en image.

        Parameters
        ----------
        dimImage : (int, int, int)
            Taille de l'image souhaitée (hauteur, largeur, profondeur).
        """
        image = np.zeros(dimImage)
        GrilleUtils.creerImage(racine=self.racine,
                               numRacine=0,
                               NW=(0, 0),
                               SE=dimImage[0:2],
                               profondeur=0,
                               image=image)
        return image

    def lectureImage(self, image):
        """
        Met à jour l'arbre à partir de l'image. Modifie l'arbre en place.

        Parameters
        ----------
        image : numpy array
            Image à partir de laquelle créer un arbre.
        """

        dimImage = image.shape
        GrilleUtils.modifierRacine(racine=self.racine,
                                  numRacine=0,
                                  NW=(0, 0),
                                  SE=dimImage[0:2],
                                  image=image)
        return None


class Noeud(object):
    """docstring for Noeud."""

    def __init__(self, grille, parent=None):
        super(Noeud, self).__init__()
        self.parent = parent
        self.grille = grille
        self.fils = []
        self._profondeur = None

    # Méthode abstraite, on supprime le fils à l'index i
    # Le noeud est modifié en place.
    def suppressionFils(self, index):
        raise NotImplementedError("La suppression d'un fils n'a pas été réimplémenté.")

    # Méthode abstraite, contraire de suppressionFils
    # Le noeud est modifié en place.
    def ajoutFils(self, nouveauFils, index, forme=None):
        raise NotImplementedError("L'ajout d'un fils n'a pas été implémenté.")


    # Implémentation abstraite de la profondeur
    @property
    def profondeur(self):
        raise NotImplementedError("Le calcul de la profondeur d'un noeud n'a pas été implémenté.")

    # Une fonction pour remplacer l'instance noeud désignée par nouveau dans son parent.
    def remplacer(self, nouveau):
        # On trouve l'indice de l'élément actuel dans la liste fils du parent
        indexParent = self.parent.fils.index(self)
        self.parent.fils[indexParent] = nouveau
        nouveau.parent = self.parent

    # Renvoie une copie de tout le sousArbre qui se trouve au dela de cette grille, mais sans parent pour ce noeud et sans grille associée.
    # Cette méthode est utile pour faire des fusions d'arbres.
    def sousArbre(self):
        raise NotImplementedError("La création d'un sous-arbre à partir d'un noeud n'a pas été implémentée.")

    # Attache un noeud et tous ses fils récursivement à une grille, en mettant au passage à jour les caractéristiques de la grille. Doit être appelé après avoir donné un parent au noeud considéré. Cette étape est utile pour garder des grilles cohérentes après les étapes de fusion.
    def attacher(self, grille):
        raise NotImplementedError("L'attachement d'un noeud à une grille n'a pas été implémentée.")



class Parallele(Noeud):
    """docstring for Parallele."""

    def __init__(self, grille, parent=None):
        super(Parallele, self).__init__(grille=grille, parent=parent)
        if grille is not None:
            # On attache pour prendre en compte les problèmes de profondeur etc... Inutile (et erroné) si la grille est None
            self.attacher(self.grille)

    # Note : les propriétés ne sont pas héritées en python...
    @property
    def profondeur(self):
        if self.parent == None:
            return 0
        elif _profondeur is None:
            _profondeur = profondeur(parent) + 1    # On mémoïse la profondeur pour éviter des calculs inutiles
        return _profondeur


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
        if taille < 2:
            # S'il ne reste plus qu'un seul bloc fils il prend la place du bloc parallèle. Il faut juste faire attention à la mémoïzation de la profondeur
            self.fils[0]._profondeur = self.profondeur
            self.replace(self.fils[0])
        self.grille.forme[self.profondeur+1] -= 1


    def ajoutFils(self, nouveauFils, index, forme=None):
        if forme is not None:
            raise NonFeuilleException("Vous ne pouvez pas changer le forme d'un noeud (non feuille) qui existe déjà avec ajoutFils !")
        elif index is None:
            raise NonFeuilleException("Vous devez préciser à quel index insérer le nouveau fils parmi les fils du noeud préexistant !")
        if index == len(self.fils):
            self.fils.append(nouveauFils)
        else:
            self.fils.insert(index, nouveauFils)
        # On met à jour la généalogie du noeud ajouté.
        nouveauFils.parent = self
        # On attache le nouveau noeud à la grille
        nouveauFils.attacher(self.grille)

    # L'algorithme de copie du sous arbre est évidemment récursif
    def sousArbre(self):
        copieNoeud = Parallele(None)
        for fils in self.fils:
            copieNoeud.fils.append(fils.sousArbre())
        return copieNoeud

    def attacher(self, grille):
        self.grille = grille
        if self.profondeur + 1 == len(self.grille.forme):
            # Comme un noeud parallèle a forcément des enfants, il faut ajouter un niveau à la forme de la grille
            self.grille.forme.append(0)
        self.grille.forme[self.profondeur] += 1
        for fils in self.fils:
            fils.attacher(grille)


class Serie(Noeud):
    """docstring for Serie."""

    def __init__(self, grille, parent=None):
        super(Serie, self).__init__(grille=grille, parent=parent)
        self.capacites = []
        self.valeurCapaciteDefaut = 1
        if grille is not None:
            # On attache pour prendre en compte les problèmes de profondeur etc... Inutile (et erroné) si la grille est None
            self.attacher(self.grille)

    # Note : les propriétés ne sont pas héritées en python...
    @property
    def profondeur(self):
        if self.parent == None:
            return 0
        elif _profondeur is None:
            _profondeur = profondeur(parent) + 1    # On mémoïse la profondeur pour éviter des calculs inutiles
        return _profondeur


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
        # On met à jour le nombre de condensateurs dans la grille
        self.grille.nbCondensateurs -= 1

        if taille < 2:
            # S'il ne reste plus qu'un seul bloc fils il prend la place du bloc série. Il faut juste faire attention à la mémoïzation de la profondeur.
            self.fils[0]._profondeur = self.profondeur
            self.replace(self.fils[0])
        # On met à jour la forme de la grille
        self.grille.forme[self.profondeur+1] -= 1


    def ajoutFils(self, nouveauFils, index=None, forme=None):
        if forme is not None:
            raise NonFeuilleException("Vous ne pouvez pas changer le forme d'un noeud (non feuille) qui existe déjà avec ajoutFils !")
        elif index is None:
            raise NonFeuilleException("Vous devez préciser à quel index insérer le nouveau fils parmi les fils du noeud préexistant !")
        taille = len(self.fils)
        # Il faut aussi aojuter une valeur de capacité intermédiaire dans le cas d'une liaison série. Attention à ne pas ajouter de capacité pour le premier fils !
        if taille > 0 and (index == taille or index == taille + 1):
            self.capacites.append(self.valeurCapaciteDefaut)
        else:
            self.capacites.insert(index, self.valeurCapaciteDefaut)
        # On met à jour le nombre de condensateurs dans la grille.
        self.grille.nbCondensateurs += 1

        # On insère le noeud dans la liste des fils.
        if index == len(self.fils):
            self.fils.append(nouveauFils)
        else:
            self.fils.insert(index, nouveauFils)
        # On met à jour la généalogie du noeud ajouté.
        nouveauFils.parent = self
        # On attache le nouveau noeud à la grille
        nouveauFils.attacher(self.grille)

    # L'algorithme de copie du sous arbre est évidemment récursif
    def sousArbre(self):
        copieNoeud = Serie(None)
        for fils in self.fils:
            copieNoeud.fils.append(fils.sousArbre())
        for i in len(self.capacites):
            copieNoeud.capacites[i] = self.capacites[i]
        return copieNoeud

    def attacher(self, grille):
        self.grille = grille
        if self.profondeur + 1 == len(self.grille.forme):
            # Comme un noeud série a forcément des enfants, il faut ajouter un niveau à la forme de la grille
            self.grille.forme.append(0)
        self.grille.forme[self.profondeur] += 1
        # Il faut aussi prendre en sompte toutes les capacités que l'on ajoute à l'arbre.
        self.grille.nbCondensateurs += len(self.capacites)
        for fils in self.fils:
            fils.attacher(grille)


class Feuille(Noeud):
    """docstring for Feuille."""

    def __init__(self, grille, parent=None):
        super(Feuille, self).__init__(grille=grille, parent=parent)
        self.H = 0
        # Qu'est ce que val ? Vous voulez sans doute parler de H = 1/R non ?
        self.val = randint(0, 42)

    # Note : les propriétés ne sont pas héritées en python...
    @property
    def profondeur(self):
        if self.parent == None:
            return 0
        else:
            # Pas de mémoïzation de la profondeur pour une feuille car elle sera amenée à changer
            return profondeur(parent) + 1

    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
        return self.H, curseur

    # Utilité ?
    # @property
    # def fini(self):
    #     raise FeuilleException("Une feuille n'a pas de fils !")

    def suppressionFils(self, index):
        raise FeuilleException("Une feuille n'a pas de fils !")

    def ajoutFils(self, nouveauFils, index=None, forme=None):
        if forme is None or forme not in ['parallele', 'serie']:
            raise FeuilleException("Pour créer un nouveau noeud à partir d'une feuille il faut préciser la forme à donner, l'un de 'parallele' ou 'serie'.")
        elif index is not None:
            raise FeuilleException("Pour créer un nouveau noeud à partir d'une feuille il ne faut pas préciser d'index, qui n'est utilisable que pour un noeud Parallele ou Serie.")
        elif forme == 'parallele':
            # Si besoin, le constructeur de Parallele changera la taille de forme pour nous
            nouveauNoeud = Parallele(grille, self.parent)
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
        elif forme == 'serie':
            # Si besoin, le constructeur de Serie changera la taille de forme pour nous
            nouveauNoeud = Serie(grille, self.parent)
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
        # On remplace cette feuille par son nouveau parent dans la généalogie de l'arbre
        self.replace(nouveauNoeud)

    # L'algorithme de copie du sous arbre est évidemment récursif
    def sousArbre(self):
        copieNoeud = Feuille(None)
        copieNoeud.H = self.H
        return copieNoeud

    def attacher(self, grille):
        self.grille = grille
        self.grille.forme[self.profondeur] += 1
        # Une feuille n'a pas de fils donc on n'a pas besoin d'appel récursif içi.


# Une erreur est apparue car vous utilisé une syntaxe invalide sur une feuille.
class FeuilleException(Exception):
    # Syntaxe spéciale pour une déclaration d'exceptions plus rapide
    pass

# Une erreur est apparue car vous avez utilisé une syntaxe spécifique aux feuilles pour un noeud.
class NonFeuilleException(Exception):
    # Syntaxe spéciale pour une déclaration d'exceptions plus rapide
    pass
