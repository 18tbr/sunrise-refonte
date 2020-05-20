# Ce fichier contient l'implémentation des noeuds de type parallèle. La documentation de toutes les méthodes des noeuds est disponible dans la classe parente.

from Noeud import Noeud

class Parallele(Noeud):
    """docstring for Parallele."""

    def __init__(self, grille=None, parent=None):
        super(Parallele, self).__init__(grille=grille, parent=parent)

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

    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
        result = 0
        for fils in self.fils:
            resultBranche, curseur = fils.creationSimulationRecursive(
                A, B, C, gauche, droite, curseur
            )
            if resultBranche is not None:
                result += resultBranche
        return result, curseur

    def creationMarquageRecursif(
        self, A, B, C, D, gauche, droite, curseur, conteneur, capaciteDroite
    ):
        if conteneur is None:
            # Si on n'est pas sous une liaison parallèle, on crée un conteneur.
            nouveauConteneur = []
        else:
            # On réutilise le conteneur du parent
            nouveauConteneur = conteneur

        result = 0
        for fils in self.fils:
            (
                delaiBranche,
                resultBranche,
                curseur,
            ) = fils.creationMarquageRecursif(
                A,
                B,
                C,
                D,
                gauche,
                droite,
                curseur,
                nouveauConteneur,
                capaciteDroite,
            )
            if resultBranche is not None:
                result += resultBranche

        if conteneur is None:
            # i.e. on n'est pas sous une liaison en paralèle, alors on résout le délai des fils.
            delai = sum(nouveauConteneur) / len(nouveauConteneur)
            return delai, result, curseur
        else:
            return None, result, curseur

    def injectionMarquage(self, E, gauche, droite, curseur, capaciteDroite):
        for fils in self.fils:
            curseur = fils.injectionMarquage(
                E, gauche, droite, curseur, capaciteDroite
            )
        return curseur

    def suppressionFils(self, index):
        # On met à jour la forme de la grille en détachant le noeud désigné.
        self.fils[index].detacher()
        # IndexError out of range si index est trop grand pour self.fils
        del self.fils[index]
        taille = len(self.fils)
        if taille < 2:
            # S'il ne reste plus qu'un seul bloc fils il prend la place du bloc parallèle. Il faut juste faire attention à la mémoïzation de la profondeur
            remplacant = self.fils[0]
            del self.fils[0]  # Pour éviter les problèmes avec détacher
            remplacant.detacher()  # On va le rattacher dans remplacer
            remplacant._profondeur = self.profondeur
            # Notez que replace appelle detacher pour nous en interne
            self.remplacer(remplacant)
            # On renvoie le noeud qui prend notre place dans l'arbre
            return remplacant
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
            copieFils = fils.sousArbre()
            copieFils.parent = copieNoeud
            copieNoeud.fils.append(copieFils)
        return copieNoeud

    def attacher(self, grille):
        if grille is not self.grille:
            self.grille = grille
            if self.profondeur + 1 == len(self.grille.forme):
                # Comme un noeud parallèle a forcément des enfants, il faut ajouter un niveau à la forme de la grille
                self.grille.forme.append(0)
            self.grille.forme[self.profondeur] += 1
            for fils in self.fils:
                fils.attacher(grille)

    def detacher(self):
        self.grille.forme[self.profondeur] -= 1
        # On détache récursivement tous les fils pour bien prendre en compte l'influence sur la forme.
        for fils in self.fils:
            fils.detacher()
        if self.grille.forme[self.profondeur + 1] == 0:
            # i.e. on a détaché tous les noeuds qui étaient à la profondeur suivante (qui est par construction la dernière de l'arbre), alors il faut l'enlever de la forme de la grille pour éviter les 0 inutiles
            self.grille.forme.pop()
        # On ne perd la référence à la grille qu'à la toute fin de la fonction car on la référence au dessus
        self.grille = None
        # On perd aussi la référence à son parent pour éviter les effets de bord étranges
        self.parent = None

    def dessiner(self, image, coinHautGauche, coinBasDroite):
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On compte le nombre de divisions qu'il faut faire sur l'image
        nombreDivisions = len(self.fils)
        # On calcule la hauteur de chaque subdivision verticale que l'on s'apprète à créer. On rappelle que le 0,0 est tout en haut à gauche de l'image.
        hauteur = int((coinBasDroiteY - coinHautGaucheY) / nombreDivisions)
        # On appelle récursivement la méthode dessiner sur les enfants
        for i in range(nombreDivisions - 1):
            fils = self.fils[i]
            coinHautGaucheFils = (coinHautGaucheY + i *hauteur, coinHautGaucheX)
            coinBasDroiteFils = (coinHautGaucheY + (i+1) *hauteur, coinBasDroiteX)
            fils.dessiner(image, coinHautGaucheFils, coinBasDroiteFils)
        # Pour être certain de bien colorer toute l'image et de ne pas laisser des bords noirs à cause de problèmes d'arrondis, on effectue la dernière coloration séparément.
        fils = self.fils[-1]
        coinHautGaucheFils = (coinHautGaucheY + (nombreDivisions-1)*hauteur, coinHautGaucheX)
        coinBasDroiteFils = (coinBasDroiteY, coinBasDroiteX)
        fils.dessiner(image, coinHautGaucheFils, coinBasDroiteFils)

    # La façon dont on calcule les moyennes pour les capacités dans cette implémentation est sans doute une source d'erreur.
    def lire(self, image, coinHautGauche, coinBasDroite):
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On compte le nombre de divisions qu'il faut faire sur l'image
        nombreDivisions = len(self.fils)
        # On calcule la hauteur de chaque subdivision verticale que l'on s'apprète à créer. On rappelle que le 0,0 est tout en haut à gauche de l'image.
        hauteur = int((coinBasDroiteY - coinHautGaucheY) / nombreDivisions)
        # Dans la mesure où l'autoencodeur ne renvoie pas la même valeur de capacité à droite pour tous les fils, nous devons en faire la moyenne ici pour conserver la cohérence par rapport à l'image et ne pas en favoriser une partie.
        propositionsCapacite = [0 for i in range(nombreDivisions)]
        # On appelle récursivement la méthode dessiner sur les enfants
        for i in range(nombreDivisions-1):
            fils = self.fils[i]
            coinHautGaucheFils = (coinHautGaucheY + i*hauteur, coinHautGaucheX)
            coinBasDroiteFils = (coinHautGaucheY + (i+1)*hauteur, coinBasDroiteX)
            propositionsCapacite[i] = fils.lire(image, coinHautGaucheFils, coinBasDroiteFils)
        # Pour être certain de bien colorer toute l'image et de ne pas laisser des bords noirs à cause de problèmes d'arrondis, on effectue la dernière coloration séparément.
        fils = self.fils[-1]
        coinHautGaucheFils = (coinHautGaucheY + (nombreDivisions-1)*hauteur, coinHautGaucheX)
        coinBasDroiteFils = (coinBasDroiteY, coinBasDroiteX)
        propositionsCapacite[-1] = fils.lire(image, coinHautGaucheFils, coinBasDroiteFils)
        # On renvoie la moyenne des valeurs des capacites proposées.
        return sum(propositionsCapacite)/len(propositionsCapacite)

    def normaliser(self, image, coinHautGauche, coinBasDroite):
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On compte le nombre de divisions qu'il faut faire sur l'image
        nombreDivisions = len(self.fils)
        # On calcule la hauteur de chaque subdivision verticale que l'on s'apprète à créer. On rappelle que le 0,0 est tout en haut à gauche de l'image.
        hauteur = int((coinBasDroiteY - coinHautGaucheY) / nombreDivisions)
        # Dans la mesure où l'autoencodeur ne renvoie pas la même valeur de capacité à droite pour tous les fils, nous devons en faire la moyenne ici pour conserver la cohérence par rapport à l'image et ne pas en favoriser une partie.
        # On appelle récursivement la méthode dessiner sur les enfants
        for i in range(nombreDivisions-1):
            fils = self.fils[i]
            coinHautGaucheFils = (coinHautGaucheY + i*hauteur, coinHautGaucheX)
            coinBasDroiteFils = (coinHautGaucheY + (i+1)*hauteur, coinBasDroiteX)
            fils.normaliser(image, coinHautGaucheFils, coinBasDroiteFils)
        # Pour être certain de bien colorer toute l'image et de ne pas laisser des bords noirs à cause de problèmes d'arrondis, on effectue la dernière coloration séparément.
        fils = self.fils[-1]
        coinHautGaucheFils = (coinHautGaucheY + (nombreDivisions-1)*hauteur, coinHautGaucheX)
        coinBasDroiteFils = (coinBasDroiteY, coinBasDroiteX)
        fils.normaliser(image, coinHautGaucheFils, coinBasDroiteFils)
