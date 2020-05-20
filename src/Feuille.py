# Ce fichier contient l'implémentation des feuilles de nos arbres (i.e. les résistances). La documentation de toutes les méthodes des noeuds est disponible dans la classe parente.

from Noeud import Noeud, conversionIndice
# Les deux imports qui suivent sont utiles pour ajoutFils
from Serie import Serie
from Parallele import Parallele
from random import random   # Initialisation de coefficients H aléatoire

class Feuille(Noeud):
    """docstring for Feuille."""

    def __init__(self, grille=None, parent=None):
        super(Feuille, self).__init__(grille=grille, parent=parent)
        self.H = random()
        # Utilisé pour colorer l'image, calculé à l'échelle de la grille par la fonction marquage.
        self._marquage = (None, None, None)

    # Note : les propriétés ne sont pas héritées en python...
    @property
    def profondeur(self):
        if self.parent == None:
            return 0
        else:
            # Pas de mémoïzation de la profondeur pour une feuille car elle sera amenée à changer
            return self.parent.profondeur + 1

    # On fait une propriété de marquage pour éviter qu'il ne soit lu plusieurs fois entre des générations par erreur.
    @property
    def marquage(self):
        if self._marquage != (None, None, None):
            result = self._marquage
            self._marquage = (None, None, None)
            return result
        else:
            raise NonMarqueException("La feuille désignée n'a pas encore été marquée.")


    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
        return self.H, curseur

    def creationMarquageRecursif(
        self, A, B, C, D, gauche, droite, curseur, conteneur, capaciteDroite
    ):
        delai = capaciteDroite / self.H
        if conteneur is not None:
            conteneur.append(delai)
        return delai, self.H, curseur

    def injectionMarquage(self, E, gauche, droite, curseur, capaciteDroite):
        indiceErreur = conversionIndice(droite)
        erreur = E[droite]
        self._marquage = (self.H, capaciteDroite, erreur)
        return curseur

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
            nouveauNoeud = Parallele()
            # On remplace cette feuille par son nouveau parent dans la généalogie de l'arbre. Si besoin, la taille de la grille sera changée automatiquement.
            self.remplacer(nouveauNoeud)
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
        elif forme == "serie":
            nouveauNoeud = Serie()
            # On remplace cette feuille par son nouveau parent dans la généalogie de l'arbre. Si besoin, la taille de la grille sera changée automatiquement.
            self.remplacer(nouveauNoeud)
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
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
        if grille is not self.grille:
            self.grille = grille
            self.grille.forme[self.profondeur] += 1
            # Une feuille n'a pas de fils donc on n'a pas besoin d'appel récursif içi.

    def detacher(self):
        self.grille.forme[self.profondeur] -= 1
        self.grille = None
        # On perd aussi la référence à son parent pour éviter les effets de bord étranges
        self.parent = None

    def dessiner(self, image, coinHautGauche, coinBasDroite):
        # On récupère le marquage de ce noeud.
        rouge, vert, bleu = self.marquage
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On colore d'abord les résistances
        image[coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 0] = rouge
        # On colore ensuite les capacités
        image[
            coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 1
        ] = vert
        # On colore enfin l'erreur
        # On colore ensuite les capacités
        image[
            coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 2
        ] = bleu


# Une erreur est apparue car vous utilisé une syntaxe invalide sur une feuille.
class FeuilleException(Exception):
    # Syntaxe spéciale pour une déclaration d'exceptions plus rapide
    pass


# Une erreur est apparue car vous avez utilisé une syntaxe spécifique aux feuilles pour un noeud.
class NonFeuilleException(Exception):
    # Syntaxe spéciale pour une déclaration d'exceptions plus rapide
    pass

# Une erreur qui signale que l'on tente de récupérer le marquage (i.e. la couleur) d'un noeud qui n'a pas encore été marqué.
class NonMarqueException(Exception):
    pass
