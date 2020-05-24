import os  # Utile pour les manipulations de fichiers.
import numpy as np  # Utile pour fournir des données à Keras.

from keras.layers import (
    Input,
    Dense,
    Conv2D,
    MaxPooling2D,
    UpSampling2D,
)  # Les éléments constitutifs de notre modèle.
from keras.models import (
    Model,
    load_model,
)  # Outils pouf manipuler des modèles Keras facilement
from keras import backend as K

from Entrainement import (
    lectureBlob,
    unificationPopulation,
)  # Des fonctions utiles pour simplifier l'entrainement non supervisé
from Autoencodeur import (
    Autoencodeur,
)  # La classe que l'on cherche à implémenter


class AutoencodeurNonDeterministe(Autoencodeur):
    """docstring for AutoencodeurNonDeterministe."""

    # Le nombre d'images à générer en même temps lors de la recherche d'une amélioration pour un autoencodeur non deterministe.
    TAILLE_GROUPE = 10

    # La proportion de la population pour laquelle on autorise l'autoencodeur non déterministe à ne pas trouver d'améliorations. Plus cette proportion est grande, plus l'amélioration est rapide mais moins elle est efficace.
    ECHEC_PERMIS = 0.1

    def __init__(
        self,
        nomDuModele="ameliorateur",
        largeur=32,
        hauteur=32,
        *args,
        **kwargs
    ):
        super(AutoencodeurNonDeterministe, self).__init__(
            nomDuModele, largeur, hauteur, *args, *kwargs
        )
        # Le constructeur est partagé avec AutoencodeurDeterministe donc on n'a rien de plus à faire ici.

    def creation(
        self, facteurReduction=2, baseDimensions=9, baseNoyau=4, baseDense=50
    ):
        # Méthode à utiliser pour créer un nouveau modèle dans le contexte d'un entrainement.

        # La meilleure configuration d'autoencodeur que j'ai trouvée pour notre problème. Il est concu pour des images de taille 32 x 32 mais d'autres configurations sont possibles.

        # On peut donner soit une liste, soit un unique coefficient dans baseDimensions, baseDense et baseNoyau. Si on donne une liste, ce sont les coefficients dans cette liste qui sont utilisés.
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

        # La fonction utilisée par la librairie Keras pour construire notre autoencodeur. Dans la notation Keras, la forme de entree est (None, hauteur, largeur, 3).
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
        # Utile pour avoir la forme de l'autoencodeur lorsque l'on fait du debuggage.
        self.autoencodeur.summary()

    def ameliorerArbres(self, listeArbres, iterations=1):
        # Cas non déterministe. Notez que dans le cas non deterministe on suppose que si un arbre relit l'image qu'il a lui même créé, il revient dans l'état où il était au moment de créer l'image (ce qui est vrai sauf problèmes d'arrondi).

        # On définit la liste des arbres et images pour lesquelles on n'a pas trouvé d'améliorations et qui va diminuer à chaque itération. Notez que l'on conserve aussi l'indice qu'à l'arbre dans la liste initiale afin de renvoyer les images dans le bon ordre à la fin de la fonction (c'est à cela que sert enumerate).
        listeArbreRestants = list(enumerate(listeArbres))
        # Ces images nous servent aussi à restaurer les arbres que nous n'avons pas réussi à améliorer à la fin de la boucle.
        listeImagesAmeliorees = [
            arbre.ecritureImage(largeur=self.largeur, hauteur=self.hauteur)
            for arbre in listeArbres
        ]
        # On a aussi besoin du score initial de tous les arbres
        listeScoresRestants = [arbre.score() for arbre in listeArbres]

        # Le seuil au dela duquel on a améliorer suffisament d'individus pour se permettre de sortir de la boucle.
        seuilTerminaison = (
            len(listeArbres) * AutoencodeurNonDeterministe.ECHEC_PERMIS
        )

        # On boucle tant que l'on a pas trouvé une amélioration pour suffisament d'arbres.
        while len(listeArbreRestants) > seuilTerminaison:
            # Avant de générer des propositions aléatoires, on récupère la liste de toutes les images restantes à traiter.
            listeImagesRestantes = []
            for indiceOrigine, arbre in listeArbreRestants:
                listeImagesRestantes.append(
                    listeImagesAmeliorees[indiceOrigine]
                )

            # On génère des propositions aléatoires.
            propositions = [
                self.autoencodeur.predict(np.array(listeImagesRestantes))
                for i in range(AutoencodeurNonDeterministe.TAILLE_GROUPE)
            ]

            for i in range(len(listeArbreRestants)):
                # indiceOrigine est l'indice qu'avait l'arbre dans la liste d'origine.
                indiceOrigine, arbre = listeArbreRestants[i]

                # L'indice de la meilleure proposition parmi toutes celles fournies de façon non deterministe
                meilleureProposition = None
                for j in range(AutoencodeurNonDeterministe.TAILLE_GROUPE):
                    # On lit l'image proposée. Le premier indice correspond au fait qu'il y a plusieurs propositions par images et le second au fait qu'il y a plusieurs images.
                    # ATTENTION, lectureImage détruit l'image lue par effet de bord. En en fait donc une copie afin de ne pas la perdre.
                    copieImage = propositions[j][i].copy()
                    arbre.lectureImage(copieImage)
                    # On calcule le nouveau score
                    scorePropose = arbre.score()
                    if scorePropose > listeScoresRestants[i]:
                        # On note l'index de la proposition
                        meilleureProposition = j
                        # On note aussi le score de la proposition dans la liste afin de pouvoir y comparer les propositions qui restent à traiter
                        listeScoresRestants[i] = scorePropose

                if meilleureProposition is not None:
                    # Si on a trouvé une proposition qui marche bien, on remet l'arbre à jour et on met l'image correpondante dans la liste à renvoyer.

                    # Ici nous n'avons pas besoin de faire de copie dde l'image, elle ne sera pas réutilisée de toute façon.
                    meilleureImage = propositions[meilleureProposition][i]
                    arbre.lectureImage(meilleureImage)
                    # On supprime l'individu des individus encore à traiter.
                    del listeArbreRestants[i]
                    del listeScoresRestants[i]
                    # Enfin, on remplace l'image d'origine par l'image améliorée dans la liste dédiée
                    listeImagesAmeliorees[indiceOrigine] = meilleureImage
                # Notez que nous n'avons rien besoin de faire sinon, l'arbre sera remis à jour correctement en lisant un image lorsque nous testerons de nouvelles propositions

        # Notez que pour tous les arbres pour lesquels nous n'avons pas trouvé de meilleure proposition, il nous faut les remettre dans leur état d'origine.
        for i in range(len(listeArbreRestants)):
            indiceOrigine, arbre = listeArbreRestants[i]
            imageOrigine = listeImagesAmeliorees[indiceOrigine]
            # On restaure l'arbre à son état initial.
            # ATTENTION, l'image utilisée est détruite par effet de bord
            arbre.lectureImage(imageOrigine)
