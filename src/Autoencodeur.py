# Ce fichier contient une classe implémentant un autoencodeur classique. Il s'agit en réalité d'un simple enrobage de la librairie Keras. Par défaut, l'autoencodeur chargé sera celui situé dans le dossier modeles avec le nom "ameliorateur.md5". Pour utiliser un autre modèle, il faut le placer dans le dossier "modele" et passer son nom au constructeur

import os  # Utile pour les manipulations de fichiers.
import numpy as np  # Utile pour fournir des données à Keras.

# On importe keras pour pouvoir utiliser notre autoencodeur
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model, load_model
from keras import backend as K

from SunRiseException import ModeleIntrouvable
from Entrainement import lectureBlob, unificationPopulation


# Cette implémentation est trop longue et incohérente, il faudrait utiliser une classe abstraite et de l'héritage pour séparer Autoencodeur déterministe et non déterministe.
class Autoencodeur(object):
    """docstring for Autoencodeur."""

    # Le nombre d'images à générer en même temps lors de la recherche d'une amélioration pour un autoencodeur non deterministe.
    TAILLE_GROUPE_NON_DETERMINISTE = 10
    # La proportion de la population pour laquelle on autorise l'autoencodeur non déterministe à ne pas trouver d'améliorations. Plus cette proportion est grande, plus l'amélioration est rapide mais moins elle est efficace.
    ECHEC_NON_DETERMINISTE = 0.1

    def __init__(
        self,
        nomDuModele="ameliorateur",
        largeur=32,
        hauteur=32,
        deterministe=True,
    ):
        super(Autoencodeur, self).__init__()
        # Pour signifier que l'on souhaite créer un nouveau modèle et non en utiliser un préexistant, utiliser la valeur None comme nomDuModele

        # Ces deux parmaètres dimensionnent les images et sont utiles dans plusieurs méthodes distinctes.
        self.largeur = largeur
        self.hauteur = hauteur

        # L'attribut deterministe détermine si l'autoencodeur considéré est classique (deterministe=True) ou variationnel i.e. un VAE (deterministe=False)
        self.deterministe = deterministe

        if nomDuModele is None:
            self.autoencodeur = None
        else:
            # sinon on charge le modèle demandé
            cheminModele = os.path.join("modeles", f"{nomDuModele}.md5")
            if os.path.exists(cheminModele):
                self.autoencodeur = load_model(cheminModele)
            else:
                raise ModeleIntrouvable(
                    f"Le modele {nomDuModele} demandé n'a pas pu être chargé, le fichier {cheminModele} n'existe pas."
                )

    def creationNouveau(
        self, facteurReduction=2, baseConvolution=9, baseNoyau=4
    ):
        # Méthode à utiliser pour créer un nouveau modèle dans le contexte d'un entrainement.

        # La meilleure configuration d'autoencodeur que j'ai trouvée pour notre problème. Il est concu pour des images de taille 32 x 32 mais d'autres configurations sont possibles.

        # La fonction utilisée par la librairie Keras pour construire notre autoencodeur. Dans la notation Keras, la forme de entree est (None, hauteur, largeur, 3).
        entree = Input(shape=(self.hauteur, self.largeur, 3))

        # x sera de taille (None, hauteur, largeur, 6)
        x = Conv2D(
            filters=1 * baseConvolution,
            kernel_size=4 * baseNoyau,
            activation="relu",
            padding="same",
        )(entree)
        # encode sera de taille (None, hauteur/2, largeur/2, 6)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(
            filters=2 * baseConvolution,
            kernel_size=3 * baseNoyau,
            activation="relu",
            padding="same",
        )(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(
            filters=3 * baseConvolution,
            kernel_size=2 * baseNoyau,
            activation="relu",
            padding="same",
        )(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(
            filters=4 * baseConvolution,
            kernel_size=1 * baseNoyau,
            activation="relu",
            padding="same",
        )(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Dense(200, activation="relu")(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Dense(100, activation="relu")(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Dense(200, activation="relu")(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(
            filters=4 * baseConvolution,
            kernel_size=1 * baseNoyau,
            activation="relu",
            padding="same",
        )(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(
            filters=3 * baseConvolution,
            kernel_size=2 * baseNoyau,
            activation="relu",
            padding="same",
        )(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(
            filters=2 * baseConvolution,
            kernel_size=3 * baseNoyau,
            activation="relu",
            padding="same",
        )(x)

        # y sera de taille (None, hauteur, largeur, 6)
        x = UpSampling2D(size=facteurReduction)(x)
        # z sera de taille (None, hauteur, largeur, 6)
        x = Conv2D(
            filters=1 * baseConvolution,
            kernel_size=4 * baseNoyau,
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

    def entrainementImitation(
        self, listeImages, iterations, tailleGroupeEntrainement
    ):
        # Méthode pour entrainer le réseau de neurones à imiter une liste d'images fournies
        if type(listeImages) is list:
            listeImages = np.array(listeImages)
        self.autoencodeur.fit(
            x=listeImages,
            y=listeImages,
            batch_size=tailleGroupeEntrainement,
            epochs=iterations,
            verbose=2,
            validation_split=0.2,
            shuffle=True,
        )

    def entrainementSupervise(
        self,
        listeImagesEntree,
        listeImagesSortie,
        iterations,
        tailleGroupeEntrainement,
    ):
        # Méthode pour entrainer le réseau de neurones d'une façon supervisée
        if type(listeImagesEntree) is list:
            listeImagesEntree = np.array(listeImagesEntree)
        if type(listeImagesSortie) is list:
            listeImagesEntree = np.array(listeImagesSortie)
        self.autoencodeur.fit(
            x=listeImagesEntree,
            y=listeImagesSortie,
            batch_size=tailleGroupeEntrainement,
            epochs=iterations,
            verbose=2,
            validation_split=0.2,
            shuffle=True,
        )

    def entrainerImitationBlob(
        self, taillePopulation, iterations, tailleGroupeEntrainement
    ):
        # Une méthode raccourcie pour entrainer le réseau à faire des imitations directement à partir des données présentes dans le dossier blob/mesures

        # On commence par récupérer les données dans blob
        listeGenetiques = lectureBlob(
            taillePopulation, generationMax=None, objectif=None
        )
        # On crée une seule grosse liste contenant tous les arbres obtenus
        sourceArbresEntrainement = unificationPopulation(listeGenetiques)
        # On récupère toutes les images de tous ces arbres
        sourceImages = [
            arbre.ecritureImage(largeur=self.largeur, hauteur=self.hauteur)
            for arbre in sourceArbresEntrainement
        ]
        # On entraine le réseau sur les images obtenues
        self.entrainementImitation(
            taillePopulation, sourceImages, iterations, tailleGroupeEntrainement
        )

    def predire(self, listeImages):
        # On utilise l'autoencodeur pour prédire des améliorations sur les images fournies en entrée.
        if type(listeImages) is list:
            listeImages = np.array(listeImages)
        return self.autoencodeur.predict(listeImages)

    def ameliorerArbres(self, listeArbres, iterations=1):
        # ameliorerArbres est une version plus haut niveau de predire qui travaille directement sur des arbres pour plus de simplicité dans l'algorithme génétique.

        if self.deterministe:
            listeImages = [
                arbre.ecritureImage(largeur=self.largeur, hauteur=self.hauteur)
                for arbre in listeArbres
            ]
            # On propose des version améliorées de toutes ces images
            listeImagesAmeliorees = self.predire(listeImages, listeArbres)

            # On répète la boucle d'amélioration autant de fois que demandé. Attention cependant, si on n'a demandé qu'une seule passe d'amélioration on n'a pas besoin de rentrer dans cette boucle (d'où le -1)
            for passe in range(iterations - 1):
                # On normalise toutes les images avec l'arbre correspondant.
                for i in range(len(listeArbres)):
                    arbre = listeArbres[i]
                    listeImagesAmeliorees[i] = arbre.normalisationImage(
                        listeImagesAmeliorees[i]
                    )
                # On améliore à nouveau les images.
                listeImagesAmeliorees = self.predire(listeImagesAmeliorees)

            # Enfin, on remet à jour tous les arbres en leur donnant des coefficients améliorés
            for i in range(len(listeArbres)):
                arbre = listeArbres[i]
                imageAmelioree = listeImagesAmeliorees[i]
                arbre.lectureImage(imageAmelioree)

            # On renvoie la liste des images améliorée (la liste des arbres à été modifiée par effet de bord)
            return listeImagesAmeliorees
        else:
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
                len(listeArbres) * Autoencodeur.ECHEC_NON_DETERMINISTE
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
                    self.predire(listeImagesRestantes)
                    for i in range(Autoencodeur.TAILLE_GROUPE_NON_DETERMINISTE)
                ]

                for i in range(len(listeArbreRestants)):
                    # indiceOrigine est l'indice qu'avait l'arbre dans la liste d'origine.
                    indiceOrigine, arbre = listeArbreRestants[i]

                    # L'indice de la meilleure proposition parmi toutes celles fournies de façon non deterministe
                    meilleureProposition = None
                    for j in range(Autoencodeur.TAILLE_GROUPE_NON_DETERMINISTE):
                        # On lit l'image proposée. Le premier indice correspond au fait qu'il y a plusieurs propositions par images et le second au fait qu'il y a plusieurs images.
                        arbre.lectureImage(propositions[j][i])
                        # On calcule le nouveau score
                        scorePropose = arbre.score()
                        if scorePropose > listeScoresRestants[i]:
                            # On note l'index de la proposition
                            meilleureProposition = j
                            # On note aussi le score de la proposition dans la liste afin de pouvoir y comparer les propositions qui restent à traiter
                            listeScoresRestants[i] = scorePropose

                    if meilleureProposition is not None:
                        # Si on a trouvé une proposition qui marche bien, on remet l'arbre à jour et on met l'image correpondante dans la liste à renvoyer.
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
                arbre.lectureImage(imageOrigine)

            # Enfin, on renvoie la liste des images améliorées, la liste des arbres est modifiée par effet de bord.
            return listeImagesAmeliorees

    def sauver(self, nomDuModele):
        # On sauvegarde le modèle actuel dans modèles sous le nom proposé. On suppose que le programme est lancé depuis la racine du dépôt git.
        cheminModele = os.path.join("src", "modeles", f"{nomDuModele}.md5")
        self.autoencodeur.save(cheminModele)
