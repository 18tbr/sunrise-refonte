"""Implémentation des feuilles de nos arbres (i.e. les résistances).

La documentation de toutes les méthodes des noeuds est disponible dans la classe
parente.
"""
from Noeud import Noeud, conversionIndice
# Les deux imports qui suivent sont utiles pour ajoutFils
from Serie import Serie
from Parallele import Parallele
import numpy as np  # Utile pour np.mean dans la lecture d'image
import Coefficients  # Utile pour s'assurer que les valeurs lues sont bien plus
# grandes que les valeurs minimales
from Coefficients import conductance  # Initialisation de coefficients H
# aléatoires


class Feuille(Noeud):
    """Classe pour les feuilles des arbres.

    Attributes
    ----------
    H : float
        Initialisation de coefficients `H` aléatoires.
    _marquage : (float, float, float)
        propriété.
    _profondeur : int
        propriété.
    """

    def __init__(self, grille=None, parent=None):
        """Initialisation de la classe."""
        super(Feuille, self).__init__(grille=grille, parent=parent)
        self.H = conductance()
        self._marquage = (None, None, None)

    # Note : les propriétés ne sont pas héritées en python...
    @property
    def profondeur(self):
        """Profondeur de la feuille.

        La profondeur de la racine est 0, celle d'un fils est égal à la
        profondeur de son parent plus 1.
        """
        if self.parent == None:
            return 0
        else:
            # Pas de mémoïzation de la profondeur pour une feuille car elle sera
            # amenée à changer
            return self.parent.profondeur + 1

    #
    @property
    def marquage(self):
        """Utilisé pour colorer l'image, calculé à l'échelle de la grille par la
        fonction marquage.

        On en fait une propriété pour éviter qu'il ne soit lu plusieurs fois
        entre des générations par erreur.

        Raises
        ------
        NonMarqueException
            Lorsque la feuille désignée n'a pas encore été marquée.
        """
        if self._marquage != (None, None, None):
            result = self._marquage
            self._marquage = (None, None, None)
            return result
        else:
            raise NonMarqueException(
                "La feuille désignée n'a pas encore été marquée."
            )

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
            # On remplace cette feuille par son nouveau parent dans la
            # généalogie de l'arbre. Si besoin, la taille de la grille sera
            # changée automatiquement.
            self.remplacer(nouveauNoeud)
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
        elif forme == "serie":
            nouveauNoeud = Serie()
            # On remplace cette feuille par son nouveau parent dans la
            # généalogie de l'arbre. Si besoin, la taille de la grille sera
            # changée automatiquement.
            self.remplacer(nouveauNoeud)
            nouveauNoeud.ajoutFils(self, index=0)
            nouveauNoeud.ajoutFils(nouveauFils, index=1)
        # Le nouveau noeud prend notre place dans la généalogie, c'est donc lui
        # que l'on renvoie.
        return nouveauNoeud

    # Pour ajouter des fils à substituerEnfants il faut d'abord en ajouter un
    # (même un faux, peu importe) avec ajoutFils, puis remplacer correctement
    # les parents du fils obtenu.
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
            # Une feuille n'a pas de fils donc on n'a pas besoin d'appel
            # récursif ici.

    def detacher(self, perdreParent=True):
        self.grille.forme[self.profondeur] -= 1
        self.grille = None
        if perdreParent:
            # On perd aussi la référence à son parent pour éviter les effets de
            # bord étranges
            self.parent = None

    def dessiner(self, image, coinHautGauche, coinBasDroite):
        # On récupère le marquage de ce noeud.
        rouge, vert, bleu = self.marquage
        # On récupère les coordonnées dont on a besoin pour colorer l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On colore d'abord les résistances
        image[
            coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 0
        ] = rouge
        # On colore ensuite les capacités
        image[
            coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 1
        ] = vert
        # On colore enfin l'erreur
        # On colore ensuite les capacités
        image[
            coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 2
        ] = bleu

    def lire(self, image, coinHautGauche, coinBasDroite, conteneur):
        # On récupère les coordonnées dont on a besoin pour lire l'image
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On calcule la moyenne des valeurs de coefficients de transmissions sur
        # la zone dédiée et on l'affecte à cette feuille.
        self.H = max(
            np.mean(
                image[
                    coinHautGaucheY:coinBasDroiteY,
                    coinHautGaucheX:coinBasDroiteX,
                    0,
                ]
            ),
            Coefficients.minH,
        )
        # On calcule la moyenne des valeurs de capacites sur la zone dediée et
        # on la renvoie. Notez que l'on a rien à faire avec l'erreur proposée,
        # elle n'est qu'un indice en entrée pour aider l'autoencodeur à faire
        # son travail.
        capaciteDroite = max(
            np.mean(
                image[
                    coinHautGaucheY:coinBasDroiteY,
                    coinHautGaucheX:coinBasDroiteX,
                    1,
                ]
            ),
            Coefficients.minC,
        )
        if conteneur is not None:
            conteneur.append(capaciteDroite)
        return capaciteDroite

    def normaliser(self, image, coinHautGauche, coinBasDroite):
        # On récupère les coordonnées dont on a besoin pour normaliser l'image.
        coinHautGaucheY, coinHautGaucheX = coinHautGauche
        coinBasDroiteY, coinBasDroiteX = coinBasDroite
        # On calcule la moyenne des valeurs de coefficients de transmissions sur
        # la zone dédiée on l'affecte à toute la zone.
        image[
            coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 0
        ] = np.mean(
            image[
                coinHautGaucheY:coinBasDroiteY,
                coinHautGaucheX:coinBasDroiteX,
                0,
            ]
        )
        # De même on normalise pour les capacités
        image[
            coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 1
        ] = np.mean(
            image[
                coinHautGaucheY:coinBasDroiteY,
                coinHautGaucheX:coinBasDroiteX,
                1,
            ]
        )
        # Et enfin pour l'erreur
        image[
            coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, 2
        ] = np.mean(
            image[
                coinHautGaucheY:coinBasDroiteY,
                coinHautGaucheX:coinBasDroiteX,
                2,
            ]
        )


class FeuilleException(Exception):
    """Une erreur est apparue car vous utilisé une syntaxe invalide sur une
    feuille."""
    pass


class NonFeuilleException(Exception):
    """Une erreur est apparue car vous avez utilisé une syntaxe spécifique aux
    feuilles pour un noeud."""
    pass


class NonMarqueException(Exception):
    """Une erreur qui signale que l'on tente de récupérer le marquage (i.e. la
    couleur) d'un noeud qui n'a pas encore été marqué."""
    pass
