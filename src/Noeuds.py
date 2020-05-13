from random import randint

# Un fichier qui contient les implémentations des différents noeuds que l'on trouve dans nos arbres.


class Noeud(object):
    """docstring for Noeud."""

    def __init__(self, grille, parent=None):
        super(Noeud, self).__init__()
        self.parent = parent
        self.grille = grille
        self.fils = []
        self._profondeur = None

    # Méthode abstraite, on supprime le fils à l'index i
    # Le noeud est modifié en place, et on renvoie le parent obtenu (car c'est plus pratique pour la mutation des arbres).
    def suppressionFils(self, index):
        raise NotImplementedError(
            "La suppression d'un fils n'a pas été réimplémenté."
        )

    # Méthode abstraite, contraire de suppressionFils
    # Le noeud est modifié en place, et on renvoie le parent obtenu (car c'est plus pratique pour l'initialisation des arbres)
    def ajoutFils(self, nouveauFils, index, forme=None):
        raise NotImplementedError("L'ajout d'un fils n'a pas été implémenté.")

    # Méthode utile pour la fusion d'arbres, elle sert à remplacer tous les enfants du noeud choisi par ceux passés en argument. Dans le cas d'un noeud série, on conserve autant de capacités que possible.
    def substituerEnfants(self, listeFils):
        raise NotImplementedError(
            "La subtitution de noeuds enfants n'a pas été réimplémentée."
        )

    # Implémentation abstraite de la profondeur
    @property
    def profondeur(self):
        raise NotImplementedError(
            "Le calcul de la profondeur d'un noeud n'a pas été implémenté."
        )

    # Une fonction pour remplacer l'instance noeud désignée par nouveau dans son parent. Il s'agit d'une méthode interne à la classe noeud qui ne doit pas être appelée de l'extérieur.
    def remplacer(self, nouveau):
        # On trouve l'indice de l'élément actuel dans la liste fils du parent
        indexParent = self.parent.fils.index(self)
        self.parent.fils[indexParent] = nouveau
        nouveau.parent = self.parent
        # On attache le nouvel élément à la grille
        nouveau.attacher(self.grille)
        # Dans la mesure où l'on a perdu notre place dans l'arbre, il faut s'en détacher.
        self.detacher()

    # Renvoie une copie de tout le sousArbre qui se trouve au dela de cette grille, mais sans parent pour ce noeud et sans grille associée.
    # Cette méthode est utile pour faire des fusions d'arbres.
    def sousArbre(self):
        raise NotImplementedError(
            "La création d'un sous-arbre à partir d'un noeud n'a pas été implémentée."
        )

    # Attache un noeud et tous ses fils récursivement à une grille, en mettant au passage à jour les caractéristiques de la grille. Doit être appelé après avoir donné un parent au noeud considéré. Cette étape est utile pour garder des grilles cohérentes après les étapes de fusion.
    def attacher(self, grille):
        raise NotImplementedError(
            "L'attachement d'un noeud à une grille n'a pas été implémentée."
        )

    # Pendant de attacher utilisé pour la suppression.
    def detacher(self):
        raise NotImplementedError(
            "Le détachement d'un noeud d'une grille n'a pas été implémenté."
        )


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
        if self.parent is None:
            return 0
        elif self.profondeur is None:
            self.profondeur = (
                self.parent.profondeur + 1
            )  # On mémoïse la profondeur pour éviter des calculs inutiles
        return self.profondeur

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
        # On met à jour la forme de la grille en détachant le noeud désigné.
        self.fils.detacher()
        # IndexError out of range si index est trop grand pour self.fils
        del self.fils[index]
        taille = len(self.fils)
        if taille < 2:
            # S'il ne reste plus qu'un seul bloc fils il prend la place du bloc parallèle. Il faut juste faire attention à la mémoïzation de la profondeur
            self.fils[0]._profondeur = self.profondeur
            # Notez que replace appelle detacher pour nous en interne
            self.replace(self.fils[0])
            # On renvoie le noeud qui prend notre place dans l'arbre
            return self.fils[0]
        else:
            return self

    def ajoutFils(self, nouveauFils, index, forme=None):
        if forme is not None:
            raise NonFeuilleException(
                "Vous ne pouvez pas changer le forme d'un noeud (non feuille) qui existe déjà avec ajoutFils !"
            )
        elif index is None:
            raise NonFeuilleException(
                "Vous devez préciser à quel index insérer le nouveau fils parmi les fils du noeud préexistant !"
            )
        if index == len(self.fils):
            self.fils.append(nouveauFils)
        else:
            self.fils.insert(index, nouveauFils)
        # On met à jour la généalogie du noeud ajouté.
        nouveauFils.parent = self
        # On attache le nouveau noeud à la grille
        nouveauFils.attacher(self.grille)
        # On garde notre place dans l'arbre, donc on renvoie self
        return self

    def substituerEnfants(self, listeFils):
        # On commence par détacher tous nos enfants
        for fils in self.fils:
            fils.detacher()
        # Puis on change la liste des noeuds enfants.
        self.fils = listeFils
        for fils in self.fils:
            # On se note comme parent dans chacun des nouveaux fils
            fils.parent = self
            # On attache le nouveau fils à la grille
            fils.attacher(self.grille)

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
        print(self.grille.forme)
        print(self.profondeur)
        self.grille.forme[self.profondeur] += 1
        for fils in self.fils:
            fils.attacher(grille)

    def detacher(self):
        self.grille.forme[self.profondeur] -= 1
        self.grille = None
        # On détache récursivement tous les fils pour bien prendre en compte l'influence sur la forme.
        for fils in self.fils:
            fils.detacher()


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
            _profondeur = (
                parent.profondeur + 1
            )  # On mémoïse la profondeur pour éviter des calculs inutiles
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
        # On met à jour la forme de la grille en détachant le noeud désigné.
        self.fils[index].detacher()
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
            # Notez que replace appelle detacher pour nous en interne
            self.replace(self.fils[0])
            # On renvoie le noeud qui prend notre place dans l'arbre
            return self.fils[0]
        else:
            return self

    def ajoutFils(self, nouveauFils, index=None, forme=None):
        if forme is not None:
            raise NonFeuilleException(
                "Vous ne pouvez pas changer le forme d'un noeud (non feuille) qui existe déjà avec ajoutFils !"
            )
        elif index is None:
            raise NonFeuilleException(
                "Vous devez préciser à quel index insérer le nouveau fils parmi les fils du noeud préexistant !"
            )
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
        # On garde notre place dans l'arbre, on se renvoie donc soi-même
        return self

    def substituerEnfants(self, listeFils):
        if len(listeFils) < 2:
            raise ValueError(
                f"Vous devez forcément donner plus de deux fils à un noeud série, mais l'argument passé pour listeFils ne comporte que {len(listeFils)} éléments."
            )
        # On commence par détacher tous nos enfants
        for fils in self.fils:
            fils.detacher()
        # Puis on change la liste des noeuds enfants.
        self.fils = listeFils
        for fils in self.fils:
            # On se note comme parent dans chacun des nouveaux fils
            fils.parent = self
            # On attache le nouveau fils à la grille
            fils.attacher(self.grille)
        # En plus de cela, il faut gérer la variation du nombre de condensateurs.
        nouveauNbCondensateurs = len(self.fils) - 1
        differenceCapacites = nouveauNbCondensateurs - len(self.capacites)
        if differenceCapacites <= 0:
            # On supprime les capacités superflues
            self.capacites = self.capacites[:nouveauNbCondensateurs]
        else:
            # On ajoute des capacités jusqu'à satisfaction
            nouvellesCapacites = [
                self.valeurCapaciteDefaut for i in differenceCapacites
            ]
            self.capacites += nouvellesCapacites
        # Enfin, il faut remettre à jour le nombre de capacités de la grille.
        self.grille.nbCondensateurs += differenceCapacites

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
        # Il faut aussi prendre en compte toutes les capacités que l'on ajoute à l'arbre.
        self.grille.nbCondensateurs += len(self.capacites)
        for fils in self.fils:
            fils.attacher(grille)

    def detacher(self):
        self.grille.forme[self.profondeur] -= 1
        # On décompte toutes les capacités de ce noeud.
        self.grille.nbCondensateurs -= len(self.capacites)
        self.grille = None
        # On détache récursivement tous les fils pour bien prendre en compte l'influence sur la forme.
        for fils in self.fils:
            fils.detacher()


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
            return self.parent.profondeur + 1

    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
        return self.H, curseur

    # Utilité ?
    # @property
    # def fini(self):
    #     raise FeuilleException("Une feuille n'a pas de fils !")

    def suppressionFils(self, index):
        raise FeuilleException("Une feuille n'a pas de fils !")

    def ajoutFils(self, nouveauFils, index=None, forme=None):
        if forme is None or forme not in ["parallele", "serie"]:
            raise FeuilleException(
                "Pour créer un nouveau noeud à partir d'une feuille il faut préciser la forme à donner, l'un de 'parallele' ou 'serie'."
            )
        elif index is not None:
            raise FeuilleException(
                "Pour créer un nouveau noeud à partir d'une feuille il ne faut pas préciser d'index, qui n'est utilisable que pour un noeud Parallele ou Serie."
            )
        elif forme == "parallele":
            # Si besoin, le constructeur de Parallele changera la taille de forme pour nous
            nouveauNoeud = Parallele(self.grille, self.parent)
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
        elif forme == "serie":
            # Si besoin, le constructeur de Serie changera la taille de forme pour nous
            nouveauNoeud = Serie(self.grille, self.parent)
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
        # On remplace cette feuille par son nouveau parent dans la généalogie de l'arbre
        self.remplacer(nouveauNoeud)
        # Le nouveau noeud prend notre place dans la généalogie, c'est donc lui que l'on renvoie.
        return nouveauNoeud

    # Pour ajouter des fils à substituerEnfants ils faut d'abord en ajouter un (même un faux, peu importe) avec ajoutFils, puis remplacer correctement les parents du fils obtenu.
    def substituerEnfants(self, listeFils):
        raise FeuilleException(
            "Vous ne pouvez pas substituer de fils a une feuille, car une feuille n'a pas de fils."
        )

    # L'algorithme de copie du sous arbre est évidemment récursif
    def sousArbre(self):
        copieNoeud = Feuille(None)
        copieNoeud.H = self.H
        return copieNoeud

    def attacher(self, grille):
        self.grille = grille
        self.grille.forme[self.profondeur] += 1
        # Une feuille n'a pas de fils donc on n'a pas besoin d'appel récursif içi.

    def detacher(self):
        self.grille.forme[self.profondeur] -= 1
        self.grille = None


# Une erreur est apparue car vous utilisé une syntaxe invalide sur une feuille.
class FeuilleException(Exception):
    # Syntaxe spéciale pour une déclaration d'exceptions plus rapide
    pass


# Une erreur est apparue car vous avez utilisé une syntaxe spécifique aux feuilles pour un noeud.
class NonFeuilleException(Exception):
    # Syntaxe spéciale pour une déclaration d'exceptions plus rapide
    pass
