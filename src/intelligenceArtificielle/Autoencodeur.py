"""Ce fichier contient une classe implémentant un autoencodeur classique.

Il s'agit en réalité d'un simple enrobage de la librairie Keras. Par défaut,
l'autoencodeur chargé sera celui situé dans le dossier modeles avec le nom
"ameliorateur.md5". Pour utiliser un autre modèle, il faut le placer dans le
dossier "modele" et passer son nom au constructeur.
"""

import os  # Utile pour les manipulations de fichiers.

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np  # Utile pour fournir des données à Keras.

# On importe keras pour pouvoir utiliser notre autoencodeur.
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model, load_model
from keras import backend as K

from intelligenceArtificielle.structureDonnees.SunRiseException import (
    ModeleIntrouvable,
)
from intelligenceArtificielle.Entrainement import (
    lectureBlob,
)  # Utile pour entrainer une population très simplement.


class Autoencodeur(object):
    """Classe abstraite pour les autoencodeurs.

    On utilise une classe abstraite et de l'héritage pour séparer Autoencodeur
    déterministe et non déterministe.

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
        **kwargs,
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
        super(Autoencodeur, self).__init__(*args, **kwargs)

        self.largeur = largeur
        self.hauteur = hauteur

        if nomDuModele is None:
            # Pour signifier que l'on souhaite créer un nouveau modèle et non en
            # utiliser un préexistant, utiliser la valeur None comme nomDuModele
            self.autoencodeur = None
        else:
            # sinon on charge le modèle demandé.
            # Pour que le package pip soit plus utilisable, on laisse aussi la possibiliter d'utiliser le chemin absolu du modèle que le souhaite utiliser. Pour différentier cela de l'autre option rapide, il faut mettre le .md5 à la fin du nom du modèle.
            if nomDuModele.endswith(".md5"):
                cheminModele = os.path.abspath(nomDuModele)
            else:
                # On suppose que l'on se trouve dans la racine du dépôt git.
                cheminModele = os.path.join("blob", "modeles", f"{nomDuModele}.md5")
            if os.path.exists(cheminModele):
                self.autoencodeur = load_model(cheminModele)
            else:
                raise ModeleIntrouvable(
                    f"Le modele {nomDuModele} demandé n'a pas pu être chargé, le fichier {cheminModele} n'existe pas."
                )

    def creation(
        self, facteurReduction=2, baseDimensions=9, baseNoyau=4, baseDense=50
    ):
        """Méthode abstraite."""
        raise NotImplementedError(
            "La création d'un nouvel autoencodeur pour son entrainement n'a pas été réimplémentée."
        )

    # Cette méthode est identique pour les différents types d'autoencodeurs,
    # on peut donc l'implémenter ici.
    def entrainement(
        self,
        listeImagesEntree,
        listeImagesSortie,
        iterations,
        tailleGroupeEntrainement,
    ):
        """Méthode pour entrainer le réseau de neurones.

        Vous pouvez parfaitemement passer la même valeur en entrée et en sortie
        pour un entrainement à l'imitation.

        Paramètres
        ----------
        listeImagesEntree : list
        listeImagesSortie : list
        iterations : int
            ou "epochs". Nombre d'itérations sur la base d'entraînement.
        tailleGroupeEntrainement : int
            ou "batchSize".
        """

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

    # Cette méthode est identique pour les différents types d'autoencodeurs,
    # on peut donc l'implémenter ici.
    def entrainementImitationBlob(
        self, Cint, taillePopulation, iterations, tailleGroupeEntrainement
    ):
        """Une méthode raccourcie pour entrainer le réseau à faire des
        imitations directement à partir des données présentes dans le dossier
        "blob/mesures".

        Paramètres
        ----------
        Cint
        taillePopulation
        iterations
        tailleGroupeEntrainement
        """

        # On commence par récupérer les données dans blob.
        # Les arbres seront élagués si possible.
        sourceArbresEntrainement = lectureBlob(
            Cint, taillePopulation, self.largeur, self.hauteur
        )

        # On récupère toutes les images de tous ces arbres.
        sourceImages = np.array(
            [
                arbre.ecritureImage(largeur=self.largeur, hauteur=self.hauteur)
                for arbre in sourceArbresEntrainement
            ]
        )
        # On entraine le réseau sur les images obtenues.
        self.entrainement(
            sourceImages, sourceImages, iterations, tailleGroupeEntrainement
        )

    def ameliorerArbres(self, listeArbres, iterations=1):
        """Méthode abstraite."""
        raise NotImplementedError(
            "La méthode d'amélioration d'une population d'arbres n'a pas été réimplémentée."
        )

    # Cette méthode est identique pour les différents types d'autoencodeurs,
    # on peut donc l'implémenter ici.
    def sauver(self, nomDuModele):
        """Sauvegarde le modèle actuel dans modèles sous le nom proposé.

        Paramètres
        ----------
        nomDuModele : str
            Nom souhaité pour la sauvegarde du modèle.
        """

        # On suppose que le programme est lancé depuis la racine du dépôt git.
        cheminModele = os.path.join("src", "modeles", f"{nomDuModele}.md5")
        self.autoencodeur.save(cheminModele)
