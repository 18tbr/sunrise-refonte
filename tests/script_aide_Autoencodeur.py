from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K

import numpy as np

class Autoencodeur(object):
    """docstring for Autoencodeur."""

    def __init__(self, tailleGroupeEntrainement = 128, largeur=100, hauteur=100, facteurReduction = 2, baseConvolution = 9, baseNoyau = 4):
        super(Autoencodeur, self).__init__()
        self.tailleGroupeEntrainement = tailleGroupeEntrainement
        # La fonction utilisée par la librairie Keras pour construire notre autoencodeur. Dans la notation Keras, la forme de entree est (None, hauteur, largeur, 3). None designe la taille du groupe d'entrainement, qui peut être spécifiée plus tard.
        entree = Input(shape=(hauteur, largeur, 3))

        # x sera de taille (None, hauteur, largeur, 6)
        x = Conv2D(filters=1*baseConvolution, kernel_size=4*baseNoyau, activation='relu', padding='same')(entree)
        # encode sera de taille (None, hauteur/2, largeur/2, 6)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(filters=2*baseConvolution, kernel_size=3*baseNoyau, activation='relu', padding='same')(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(filters=3*baseConvolution, kernel_size=2*baseNoyau, activation='relu', padding='same')(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Conv2D(filters=4*baseConvolution, kernel_size=1*baseNoyau, activation='relu', padding='same')(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Dense(200, activation='relu')(x)
        x = MaxPooling2D(pool_size=facteurReduction, strides=None)(x)

        x = Dense(100, activation='relu')(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Dense(200, activation='relu')(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(filters=4*baseConvolution, kernel_size=1*baseNoyau, activation='relu', padding='same')(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(filters=3*baseConvolution, kernel_size=2*baseNoyau, activation='relu', padding='same')(x)

        x = UpSampling2D(size=facteurReduction)(x)
        x = Conv2D(filters=2*baseConvolution, kernel_size=3*baseNoyau, activation='relu', padding='same')(x)

        # y sera de taille (None, hauteur, largeur, 6)
        x = UpSampling2D(size=facteurReduction)(x)
        # z sera de taille (None, hauteur, largeur, 6)
        x = Conv2D(filters=1*baseConvolution, kernel_size=4*baseNoyau, activation='relu', padding='same')(x)

        # decode sera de taille (None, hauteur, largeur, 3)
        decode = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

        # On compile le modèle créé.
        self.autoencodeur = Model(entree, decode)
        self.autoencodeur.compile(optimizer='adadelta', loss='binary_crossentropy')
        # Utile pour avoir la forme de l'autoencodeur lorsque l'on fait du debuggage.
        self.autoencodeur.summary()

    def entrainer(self, listeImages, iterations):
        if type(listeImages) is list:
            listeImages = np.array(listeImages)
        self.autoencodeur.fit(x=listeImages, y=listeImages, batch_size=self.tailleGroupeEntrainement, epochs=iterations, verbose=2, validation_split=0.2, shuffle=True)

    def predire(self, listeImages):
        if type(listeImages) is list:
            listeImages = np.array(listeImages)
        return self.autoencodeur.predict(listeImages)

    def sauver(self, nomDuFichier):
        self.autoencodeur.save(nomDuFichier)
