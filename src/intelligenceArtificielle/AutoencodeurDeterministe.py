"""Ce fichier contient une implémentation déterministe de la classe abstraite
Autoencodeur (c'est à dire des autoencodeurs classiques).
"""
import os  # Utile pour les manipulations de fichiers.
import numpy as np  # Utile pour fournir des données à Keras.

from keras.layers import (
    Input,
    Dense,
    Conv2D,
    MaxPooling2D,
    UpSampling2D,
)  # Eléments constitutifs de notre réseau de neurones
from keras.models import (
    Model,
    load_model,
)  # Outils pour manipuler facilement des modèles
from keras import backend as K

from intelligenceArtificielle.Autoencodeur import (
    Autoencodeur,
)  # La classe que l'on cherche à implémenter


class AutoencodeurDeterministe(Autoencodeur):
    """Classe pour les autoencodeurs déterministes.

    Attributs
    ---------
    largeur : int
        Dimension des images. Utile dans plusieurs méthodes distinctes.
    hauteur : int
        Dimension des images. Utile dans plusieurs méthodes distinctes.
    autoencodeur : modèle Keras
        Modèle choisi.
    """

    def __init__(
        self,
        nomDuModele="ameliorateur",
        largeur=32,
        hauteur=32,
        *args,
        **kwargs
    ):
        """Initialisation de la classe.

        Paramètres
        ----------
        nomDuModele : str
            Nom du moèle à charger. None si l'on ne souhaite pas charger de
            modèle. On ira charger le fichier "src/modeles/nomDuModele.h5".
        largeur : int
        hauteur : int

        Exceptions levées
        -----------------
        ModeleIntrouvable
            Lorsque nomDuModèle.h5 n'a pas pu être trouvé.
        """
        super(AutoencodeurDeterministe, self).__init__(
            nomDuModele, largeur, hauteur, *args, *kwargs
        )
        # Le constructeur est hérité de Autoencodeur, rien de plus à faire ici

    def creation(
        self, facteurReduction=2, baseDimensions=9, baseNoyau=4, baseDense=50
    ):
        """Méthode à utiliser pour créer un nouveau modèle dans le contexte d'un
        entrainement.

        La meilleure configuration d'autoencodeur que j'ai trouvée pour notre
        problème. Il est concu pour des images de taille 32 x 32 mais d'autres
        configurations sont possibles.

        Paramètres
        ----------
        facteurReduction : int
            ou "pool_size". Facteur de réduction pour les convolutions du
            réseau.
        baseDimensions : int | list
            Dimensions des filtres de convolution du réseau.
        baseDense : int | list
            Dimensions pour les filtres "Dense" du réseau.
        baseNoyau : int | list
            ou "kernel_size". Dimensions des noyaux de convolution du réseau.

        Notes
        -----
        On peut donner soit une liste, soit un unique coefficient dans
        `baseDimensions`, `baseDense` et `baseNoyau`. Si on donne une liste, ce
        sont les coefficients dans cette liste qui sont utilisés.
        """

        # Pour baseDimensions
        if type(baseDimensions) is list:
            dimensions = baseDimensions[:4]
        else:
            # On a fourni un unique coefficent en argument
            dimensions = [i * baseDimensions for i in range(1, 5)]

        # De même pour baseNoyau
        if type(baseNoyau) is list:
            noyau = baseNoyau[:4]
        else:
            noyau = [(5 - i) * baseNoyau for i in range(1, 5)]

        # Et enfin pour baseDense
        if type(baseDense) is list:
            dense = baseDense[:2]
        else:
            dense = [2 * baseDense, baseDense]

        # La fonction utilisée par la librairie Keras pour construire notre
        # autoencodeur. Dans la notation Keras, la forme de entree est
        # (None, hauteur, largeur, 3).
        entree = Input(shape=(self.hauteur, self.largeur, 3))

        # x sera de taille (None, hauteur, largeur, 6)
        x = Conv2D(
            filters=dimensions[0],
            kernel_size=noyau[0],
            activation="relu",
            padding="same",
        )(entree)
        # encode sera de taille (None, hauteur/2, largeur/2, 6)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(
            filters=dimensions[1],
            kernel_size=noyau[1],
            activation="relu",
            padding="same",
        )(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(
            filters=dimensions[2],
            kernel_size=noyau[2],
            activation="relu",
            padding="same",
        )(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(
            filters=dimensions[3],
            kernel_size=noyau[3],
            activation="relu",
            padding="same",
        )(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Dense(dense[0], activation="relu")(x)
        # x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Dense(dense[1], activation="relu")(x)

        # x = UpSampling2D(size=facteurReduction)(x)
        x = Dense(dense[0], activation="relu")(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(
            filters=dimensions[3],
            kernel_size=noyau[3],
            activation="relu",
            padding="same",
        )(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(
            filters=dimensions[2],
            kernel_size=noyau[2],
            activation="relu",
            padding="same",
        )(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(
            filters=dimensions[1],
            kernel_size=noyau[1],
            activation="relu",
            padding="same",
        )(x)

        # y sera de taille (None, hauteur, largeur, 6)
        x = UpSampling2D(size=facteurReduction)(x)
        # z sera de taille (None, hauteur, largeur, 6)
        x = Conv2D(
            filters=dimensions[0],
            kernel_size=noyau[0],
            activation="relu",
            padding="same",
        )(x)

        # decode sera de taille (None, hauteur, largeur, 3)
        decode = Conv2D(3, (3, 3), activation="sigmoid", padding="same")(x)

        # On compile le modèle créé.
        self.autoencodeur = Model(entree, decode)
        self.autoencodeur.compile(
            optimizer="adadelta", loss="binary_crossentropy"
        )
        # Utile pour avoir la forme de l'autoencodeur lorsque l'on debug.
        self.autoencodeur.summary()

    def ameliorerArbres(self, listeArbres, iterations=1):
        """Version plus haut niveau de `predire` qui travaille directement sur
        des arbres pour plus de simplicité dans l'algorithme génétique.

        Paramètres
        ----------
        listeArbres : list
        iterations : int
        """

        # On crée les images de tous nos arbres
        listeImages = np.array(
            [
                arbre.ecritureImage(largeur=self.largeur, hauteur=self.hauteur)
                for arbre in listeArbres
            ]
        )
        # On propose des version améliorées de toutes ces images
        listeImagesAmeliorees = self.autoencodeur.predict(listeImages)

        # On répète la boucle d'amélioration autant de fois que demandé.
        # Attention cependant, si on n'a demandé qu'une seule passe
        # d'amélioration on n'a pas besoin de rentrer dans cette boucle
        # (d'où le -1)
        for passe in range(iterations - 1):
            # On normalise toutes les images avec l'arbre correspondant.
            for i in range(len(listeArbres)):
                arbre = listeArbres[i]
                listeImagesAmeliorees[i] = arbre.normalisationImage(
                    listeImagesAmeliorees[i]
                )
            # On améliore à nouveau les images.
            listeImagesAmeliorees = self.autoencodeur.predict(
                listeImagesAmeliorees
            )

        # Enfin, on remet à jour tous les arbres en leur donnant des
        # coefficients améliorés.
        for i in range(len(listeArbres)):
            arbre = listeArbres[i]
            imageAmelioree = listeImagesAmeliorees[i]
            # ATTENTION, la méthode `lectureImage` détruit l'image passée en
            # argument.
            arbre.lectureImage(imageAmelioree)
