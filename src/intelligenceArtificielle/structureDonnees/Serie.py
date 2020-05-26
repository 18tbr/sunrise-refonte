# Ce fichier contient l'implémentation des noeuds de type série. La documentation de toutes les méthodes des noeuds est disponible dans la classe parente.

from random import randrange  # Utile pour un élaguage aléatoire

from intelligenceArtificielle.structureDonnees.Noeud import (
    Noeud,
    conversionIndice,
)
from intelligenceArtificielle.structureDonnees.Coefficients import (
    capacite,
)  # Détermination aléatoire des valeurs de capacités
from intelligenceArtificielle.structureDonnees.SunRiseException import (
    NonFeuilleException,
    ImageTropPetite,
)


class Serie(Noeud):
    """docstring for Serie."""

    def __init__(self, arbre=None, parent=None):
        self.capacites = []
        # self.valeurCapaciteDefaut = 1 # Obsolete, remplacé par une propriété
        # Attacher fait référence à capacites et le constructeur parent fait référence à attacher, donc il faut forcément appeller le constructeur parent en dernier.
        super(Serie, self).__init__(arbre=arbre, parent=parent)

    # Note : les propriétés ne sont pas héritées en python...
    @property
    def profondeur(self):
        if self.parent is None:
            return 0
        elif self._profondeur is None:
            self._profondeur = (
                self.parent.profondeur + 1
            )  # On mémoïse la profondeur pour éviter des calculs inutiles
        return self._profondeur

    @property
    def valeurCapaciteDefaut(self):
        return capacite()

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
                if gaucheBranche is None:
                    A[droiteBranche, droiteBranche] += result
                    B[droiteBranche, 0] = -result
                else:
                    # Termes hors diagonale
                    A[gaucheBranche, droiteBranche] = -result
                    A[droiteBranche, gaucheBranche] = -result
                    # Termes diagonaux
                    A[droiteBranche, droiteBranche] += result
                    A[gaucheBranche, gaucheBranche] += result
            if i + 1 < len(self.fils):
                C[droiteBranche, droiteBranche] /= self.capacites[i]
        return None, curseur

    def creationMarquageRecursif(
        self, A, B, C, D, gauche, droite, curseur, conteneur, capaciteDroite
    ):
        listeTemperatures = [gauche]
        listeCapacite = []
        for i in range(len(self.capacites)):
            curseur += 1
            listeTemperatures.append(curseur)
            listeCapacite.append(self.capacites[i])
        listeTemperatures.append(droite)
        listeCapacite.append(capaciteDroite)

        delai = 0
        for i in range(len(self.fils)):
            gaucheBranche = listeTemperatures[i]
            droiteBranche = listeTemperatures[i + 1]
            capaciteBranche = listeCapacite[i]
            delaiBranche, resultBranche, curseur = self.fils[
                i
            ].creationMarquageRecursif(
                A,
                B,
                C,
                D,
                gaucheBranche,
                droiteBranche,
                curseur,
                None,
                capaciteBranche,
            )
            if resultBranche is not None:
                # Text (i.e. gauche is None) a un traitement différent
                if gaucheBranche is None:
                    A[droiteBranche, droiteBranche] += resultBranche
                    B[droiteBranche, 0] = -resultBranche
                else:
                    # Termes hors diagonale
                    A[gaucheBranche, droiteBranche] = -resultBranche
                    A[droiteBranche, gaucheBranche] = -resultBranche
                    # Termes diagonaux
                    A[droiteBranche, droiteBranche] += resultBranche
                    A[gaucheBranche, gaucheBranche] += resultBranche

            if delaiBranche is not None:
                di = conversionIndice(gaucheBranche)
                dj = conversionIndice(droiteBranche)
                D[di, dj] = delaiBranche
                D[dj, di] = delaiBranche
                delai += delaiBranche

            if i + 1 < len(self.fils):
                C[droiteBranche, droiteBranche] /= self.capacites[i]

        if conteneur is not None:
            conteneur.append(delai)

        return delai, None, curseur

    def injectionMarquage(self, E, gauche, droite, curseur, capaciteDroite):
        listeTemperatures = [gauche]
        listeCapacite = []
        for i in range(len(self.capacites)):
            curseur += 1
            listeTemperatures.append(curseur)
            listeCapacite.append(self.capacites[i])
        listeTemperatures.append(droite)
        listeCapacite.append(capaciteDroite)

        for i in range(len(self.fils)):
            gaucheBranche = listeTemperatures[i]
            droiteBranche = listeTemperatures[i + 1]
            capaciteBranche = listeCapacite[i]
            curseur = self.fils[i].injectionMarquage(
                E, gaucheBranche, droiteBranche, curseur, capaciteBranche
            )

        return curseur

    def suppressionFils(self, index):
        # On met à jour la forme de l'arbre en détachant le noeud désigné.
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
        # On met à jour le nombre de condensateurs dans l'arbre
        self.arbre.nbCondensateurs -= 1

        if taille < 2:
            # S'il ne reste plus qu'un seul bloc fils il prend la place du bloc serie. Il faut juste faire attention à la mémoïzation de la profondeur
            remplacant = self.fils[0]
            del self.fils[0]  # Pour éviter les problèmes avec détacher
            remplacant.detacher()  # On va le rattacher dans remplacer
            remplacant._profondeur = self.profondeur
            # Notez que remplacer appelle detacher pour nous en interne
            self.remplacer(remplacant)
            # On renvoie le noeud qui prend notre place dans l'arbre
            return remplacant
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
        if taille != 0:
            if index == taille or index == taille + 1:
                self.capacites.append(self.valeurCapaciteDefaut)
            else:
                self.capacites.insert(index, self.valeurCapaciteDefaut)
            # On met à jour le nombre de condensateurs dans l'arbre.
            self.arbre.nbCondensateurs += 1

        # On insère le noeud dans la liste des fils.
        if index == len(self.fils):
            self.fils.append(nouveauFils)
        else:
            self.fils.insert(index, nouveauFils)
        # On met à jour la généalogie du noeud ajouté.
        nouveauFils.parent = self
        # On attache le nouveau noeud à l'arbre
        nouveauFils.attacher(self.arbre)
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
            # On attache le nouveau fils à l'arbre
            fils.attacher(self.arbre)
        # En plus de cela, il faut gérer la variation du nombre de condensateurs.
        nouveauNbCondensateurs = len(self.fils) - 1
        differenceCapacites = nouveauNbCondensateurs - len(self.capacites)
        if differenceCapacites <= 0:
            # On supprime les capacités superflues
            self.capacites = self.capacites[:nouveauNbCondensateurs]
        else:
            # On ajoute des capacités jusqu'à satisfaction
            nouvellesCapacites = [
                self.valeurCapaciteDefaut for i in range(differenceCapacites)
            ]
            self.capacites += nouvellesCapacites
        # Enfin, il faut remettre à jour le nombre de capacités de l'arbre.
        self.arbre.nbCondensateurs += differenceCapacites

    # L'algorithme de copie du sous arbre est évidemment récursif
    def sousArbre(self):
        copieNoeud = Serie(None)
        for fils in self.fils:
            copieFils = fils.sousArbre()
            copieFils.parent = copieNoeud
            copieNoeud.fils.append(copieFils)
        for valeurCapacite in self.capacites:
            copieNoeud.capacites.append(valeurCapacite)
        return copieNoeud

    def attacher(self, arbre):
        if arbre is not self.arbre:
            self.arbre = arbre
            if self.profondeur + 1 == len(self.arbre.forme):
                # Comme un noeud série a forcément des enfants, il faut ajouter un niveau à la forme de l'arbre
                self.arbre.forme.append(0)
            self.arbre.forme[self.profondeur] += 1
            # Il faut aussi prendre en compte toutes les capacités que l'on ajoute à l'arbre.
            self.arbre.nbCondensateurs += len(self.capacites)
            for fils in self.fils:
                fils.attacher(arbre)

    def detacher(self, perdreParent=True):
        self.arbre.forme[self.profondeur] -= 1
        # On détache récursivement tous les fils pour bien prendre en compte l'influence sur la forme.
        for fils in self.fils:
            fils.detacher(perdreParent=False)
        # On décompte toutes les capacités de ce noeud.
        self.arbre.nbCondensateurs -= len(self.capacites)
        if self.arbre.forme[self.profondeur + 1] == 0:
            # i.e. on a détaché tous les noeuds qui étaient à la profondeur suivante (qui est par construction la dernière de l'arbre), alors il faut l'enlever de la forme de l'arbre pour éviter les 0 inutiles
            self.arbre.forme.pop()
        # On ne perd la référence à l'arbre qu'à la toute fin de la fonction car on la référence au dessus
        self.arbre = None
        # On perd aussi la mémoïzation de la profondeur pour éviter de la réutiliser si on est à l'intérieur d'un sous arbre qui est déplacé
        self._profondeur = None
        if perdreParent:
            # On perd aussi la référence à son parent pour éviter les effets de bord étranges
            self.parent = None

    def dessiner(self, image, coinHautGauche, coinBasDroite):
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On compte le nombre de divisions qu'il faut faire sur l'image
        nombreDivisions = len(self.fils)
        # On calcule la largeur de chaque subdivision horizontale que l'on s'apprète à créer. On rappelle que le 0,0 est tout en haut à gauche de l'image.
        largeur = int((coinBasDroiteX - coinHautGaucheX) / nombreDivisions)
        if largeur == 0:
            raise ImageTropPetite(
                f"La largeur d'une liaison série écrite à la profondeur {self.profondeur} serait 0, la forme de l'arbre est {self.arbre.forme}"
            )
        # On appelle récursivement la méthode dessiner sur les enfants
        for i in range(nombreDivisions - 1):
            fils = self.fils[i]
            coinHautGaucheFils = (
                coinHautGaucheY,
                coinHautGaucheX + i * largeur,
            )
            coinBasDroiteFils = (
                coinBasDroiteY,
                coinHautGaucheX + (i + 1) * largeur,
            )
            fils.dessiner(image, coinHautGaucheFils, coinBasDroiteFils)
        # Pour être certain de bien colorer toute l'image et de ne pas laisser des bords noirs à cause de problèmes d'arrondis, on effectue la dernière coloration séparément.
        fils = self.fils[-1]
        coinHautGaucheFils = (
            coinHautGaucheY,
            coinHautGaucheX + (nombreDivisions - 1) * largeur,
        )
        coinBasDroiteFils = (coinBasDroiteY, coinBasDroiteX)
        fils.dessiner(image, coinHautGaucheFils, coinBasDroiteFils)

    def lire(self, image, coinHautGauche, coinBasDroite, conteneur):
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On compte le nombre de divisions qu'il faut faire sur l'image
        nombreDivisions = len(self.fils)
        # On calcule la largeur de chaque subdivision horizontale que l'on s'apprète à créer. On rappelle que le 0,0 est tout en haut à gauche de l'image.
        largeur = int((coinBasDroiteX - coinHautGaucheX) / nombreDivisions)
        if largeur == 0:
            raise ImageTropPetite(
                f"La largeur d'une liaison série écrite à la profondeur {self.profondeur} serait 0, la forme de l'arbre est {self.arbre.forme}"
            )
        # On appelle récursivement la méthode dessiner sur les enfants
        for i in range(nombreDivisions - 1):
            fils = self.fils[i]
            coinHautGaucheFils = (
                coinHautGaucheY,
                coinHautGaucheX + i * largeur,
            )
            coinBasDroiteFils = (
                coinBasDroiteY,
                coinHautGaucheX + (i + 1) * largeur,
            )
            # On met à jour la capacité à droite du fils avec la valeur renvoyée par lire
            self.capacites[i] = fils.lire(
                image, coinHautGaucheFils, coinBasDroiteFils, conteneur=None
            )
        # Pour être certain de bien colorer toute l'image et de ne pas laisser des bords noirs à cause de problèmes d'arrondis, on effectue la dernière coloration séparément.
        fils = self.fils[-1]
        coinHautGaucheFils = (
            coinHautGaucheY,
            coinHautGaucheX + (nombreDivisions - 1) * largeur,
        )
        coinBasDroiteFils = (coinBasDroiteY, coinBasDroiteX)
        capaciteDroite = fils.lire(
            image, coinHautGaucheFils, coinBasDroiteFils, conteneur=None
        )
        if conteneur is not None:
            conteneur.append(capaciteDroite)
        return capaciteDroite

    def normaliser(self, image, coinHautGauche, coinBasDroite):
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On compte le nombre de divisions qu'il faut faire sur l'image
        nombreDivisions = len(self.fils)
        # On calcule la largeur de chaque subdivision horizontale que l'on s'apprète à créer. On rappelle que le 0,0 est tout en haut à gauche de l'image.
        largeur = int((coinBasDroiteX - coinHautGaucheX) / nombreDivisions)
        if largeur == 0:
            raise ImageTropPetite(
                f"La largeur d'une liaison série écrite à la profondeur {self.profondeur} serait 0, la forme de l'arbre est {self.arbre.forme}"
            )
        # On appelle récursivement la méthode dessiner sur les enfants
        for i in range(nombreDivisions - 1):
            fils = self.fils[i]
            coinHautGaucheFils = (
                coinHautGaucheY,
                coinHautGaucheX + i * largeur,
            )
            coinBasDroiteFils = (
                coinBasDroiteY,
                coinHautGaucheX + (i + 1) * largeur,
            )
            # On met à jour la capacité à droite du fils avec la valeur renvoyée par lire
            fils.normaliser(image, coinHautGaucheFils, coinBasDroiteFils)
        # Pour être certain de bien colorer toute l'image et de ne pas laisser des bords noirs à cause de problèmes d'arrondis, on effectue la dernière coloration séparément.
        fils = self.fils[-1]
        coinHautGaucheFils = (
            coinHautGaucheY,
            coinHautGaucheX + (nombreDivisions - 1) * largeur,
        )
        coinBasDroiteFils = (coinBasDroiteY, coinBasDroiteX)
        fils.normaliser(image, coinHautGaucheFils, coinBasDroiteFils)

    def elaguerSousArbre(self, coinHautGauche, coinBasDroite):
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On compte le nombre de divisions qu'il faut faire sur l'image
        nombreDivisions = len(self.fils)
        # On suppose que la largeur allouée est supérieure à 0
        largeurAllouee = coinBasDroiteX - coinHautGaucheX
        largeur = int(largeurAllouee / nombreDivisions)
        while largeur == 0 and len(self.fils) > 2:
            index = randrange(len(self.fils))
            self.suppressionFils(index)
            largeur = int(largeurAllouee / nombreDivisions)

        if largeur == 0:
            # Si on sort de la boucle et que la largeur allouée n'est toujours pas suffisante, alors on se fait remplacer par son dernier fils. Comme on a supposé que la largeur allouée est plus grande que 0, le problème va se poser récursivement sur le dernier fils.
            index = randrange(len(self.fils))
            # On remarque que les deux seules valeurs possibles sont 0 et 1. Or si on tire 1, 1-1 = 0 désigne le dernier enfant et de même pour 0, 0-1 = -1 désigne bien l'autre enfant.
            dernierFils = self.fils[index - 1]
            self.suppressionFils(index)
            # On appelle récursivement l'élaguage sur le dernier fils (qui a pris notre place).
            dernierFils.elaguerSousArbre(coinHautGauche, coinBasDroite)
        else:
            # On a trouvé de la place pour tous les enfants, il faut de même qu'eux fassent tenir leurs sous arbres.
            for i in range(len(self.fils) - 1):
                fils = self.fils[i]
                coinHautGaucheFils = (
                    coinHautGaucheY,
                    coinHautGaucheX + i * largeur,
                )
                coinBasDroiteFils = (
                    coinBasDroiteY,
                    coinHautGaucheX + (i + 1) * largeur,
                )
                # On met à jour la capacité à droite du fils avec la valeur renvoyée par lire
                fils.elaguerSousArbre(coinHautGaucheFils, coinBasDroiteFils)
            # Pour être certain de bien colorer toute l'image et de ne pas laisser des bords noirs à cause de problèmes d'arrondis, on effectue la dernière coloration séparément.
            fils = self.fils[-1]
            coinHautGaucheFils = (
                coinHautGaucheY,
                coinHautGaucheX + (nombreDivisions - 1) * largeur,
            )
            coinBasDroiteFils = (coinBasDroiteY, coinBasDroiteX)
            fils.elaguerSousArbre(coinHautGaucheFils, coinBasDroiteFils)
