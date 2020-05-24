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

    def __init__(
        self,
        nomDuModele="ameliorateur",
        largeur=32,
        hauteur=32,
        *args,
        **kwargs
    ):
        super(Autoencodeur, self).__init__(*args, **kwargs)
        # Pour signifier que l'on souhaite créer un nouveau modèle et non en utiliser un préexistant, utiliser la valeur None comme nomDuModele

        # Ces deux parmaètres dimensionnent les images et sont utiles dans plusieurs méthodes distinctes.
        self.largeur = largeur
        self.hauteur = hauteur

        if nomDuModele is None:
            self.autoencodeur = None
        else:
            # sinon on charge le modèle demandé. On suppose que l'on se trouve dans la racine du dépôt git
            cheminModele = os.path.join("src", "modeles", f"{nomDuModele}.md5")
            if os.path.exists(cheminModele):
                self.autoencodeur = load_model(cheminModele)
            else:
                raise ModeleIntrouvable(
                    f"Le modele {nomDuModele} demandé n'a pas pu être chargé, le fichier {cheminModele} n'existe pas."
                )

    def creation(
        self, facteurReduction=2, baseDimensions=9, baseNoyau=4, baseDense=50
    ):
        raise NotImplementedError("La création d'un nouvel autoencodeur pour son entrainement n'a pas été réimplémentée.")

    # La fonction d'entrainement est partagée entre les différents types d'autoencodeurs et est donc implémentée ici.
    def entrainement(
        self,
        listeImagesEntree,
        listeImagesSortie,
        iterations,
        tailleGroupeEntrainement,
    ):
        # Méthode pour entrainer le réseau de neurones. Vous pouvez parfaitemement passer la même valeur en entrée et en sortie pour un entrainement à l'imitation
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

    # Cette méthode est partagée pour les autoencodeurs déterministes et non déterministe et est donc implémentée ici.
    def entrainementImitationBlob(
        self, Cint, taillePopulation, iterations, tailleGroupeEntrainement
    ):
        # Une méthode raccourcie pour entrainer le réseau à faire des imitations directement à partir des données présentes dans le dossier blob/mesures.

        # On commence par récupérer les données dans blob
        listeGenetiques = lectureBlob(
            Cint, taillePopulation, generationMax=None, objectif=None
        )
        # On crée une seule grosse liste contenant tous les arbres obtenus
        sourceArbresEntrainement = unificationPopulation(listeGenetiques)
        # Avant de créer les images, on élague tous les arbres.
        for arbre in sourceArbresEntrainement:
            arbre.elaguer(largeur=self.largeur, hauteur=self.hauteur)
        
        # On récupère toutes les images de tous ces arbres
        sourceImages = np.array([
            arbre.ecritureImage(largeur=self.largeur, hauteur=self.hauteur)
            for arbre in sourceArbresEntrainement
        ])
        # On entraine le réseau sur les images obtenues
        self.entrainement(
            sourceImages, sourceImages, iterations, tailleGroupeEntrainement
        )


    def ameliorerArbres(self, listeArbres, iterations=1):
        # ameliorerArbres est une version plus haut niveau de predire qui travaille directement sur des arbres pour plus de simplicité dans l'algorithme génétique.
        raise NotImplementedError("La méthode d'amélioration d'une population d'arbres n'a pas été réimplémentée.")

    # Cette méthode est identique pour tous les types d'autoencodeurs, on peut donc l'implémenter ici.
    def sauver(self, nomDuModele):
        # On sauvegarde le modèle actuel dans modèles sous le nom proposé. On suppose que le programme est lancé depuis la racine du dépôt git.
        cheminModele = os.path.join("src", "modeles", f"{nomDuModele}.md5")
        self.autoencodeur.save(cheminModele)
