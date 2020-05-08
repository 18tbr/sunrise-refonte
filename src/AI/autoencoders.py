"""
Script python pour l'implémentation de l'autoencoder.
Etapes à coder :

1. Transformation d'un arbre en image et vice-versa
    - création d'une classe Translate par exemple qui
    permet de passer de l'un à l'autre et réciproquement
    - pour cela, suivre l'algorithme de la vidéo de vincent
2. Ecriture du réseau de l'autoencoder qui prend une image en entrée
    - cf tutos envoyés par vincent
    - dans un premier temps, autoencoder simple
    - dans un second temps, VAE

"""
import os
import numpy as np
import matplotlib.pyplot as plt
import keras
import json

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # model will be trained on CPU
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model, load_model


class Autoencoder(object):
    """docstring for Autoencoder"""

    def __init__(self, inChannel=1, x=28, y=28, load_model_name=None):
        super(Autoencoder, self).__init__()

        self.inChannel = inChannel
        self.x = x
        self.y = y

        # input image dimensions are fixed and do not depend of the model
        self.input_img = Input(
            shape=(self.x, self.y, self.inChannel)
        )  # 28 x 28 x 1

        if load_model_name is None:
            self.autoencoder_model = self._create_autoencoder_model(
                self.input_img
            )
        else:
            self.autoencoder_model = self._load_model(load_model_name)

    def __str__(self):
        """
        Prettily display model
        """
        self.autoencoder_model.summary()
        return ""

    def _autoencode(self, input_img):
        """
        Encode and decode input_img
        """
        # encode
        conv1 = Conv2D(32, (3, 3), activation="relu", padding="same")(
            input_img
        )  # 28 x 28 x  32
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)  # 14 x 14 x  32
        conv2 = Conv2D(64, (3, 3), activation="relu", padding="same")(
            pool1
        )  # 14 x 14 x  64
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)  #  7 x  7 x  64
        encoded = Conv2D(128, (3, 3), activation="relu", padding="same")(
            pool2
        )  #  7 x  7 x 128

        # decode
        conv4 = Conv2D(128, (3, 3), activation="relu", padding="same")(
            encoded
        )  #  7 x  7 x 128
        up1 = UpSampling2D((2, 2))(conv4)  # 14 x 14 x 128
        conv5 = Conv2D(64, (3, 3), activation="relu", padding="same")(
            up1
        )  # 14 x 14 x  64
        up2 = UpSampling2D((2, 2))(conv5)  # 28 x 28 x  64
        decoded = Conv2D(1, (3, 3), activation="sigmoid", padding="same")(
            up2
        )  # 28 x 28 x   1

        return decoded

    def _create_autoencoder_model(self, input_img):
        """
        Return autoencoder
        """
        model = Model(inputs=input_img, outputs=self._autoencode(input_img))
        model.compile(optimizer="sgd", loss="mean_squared_error")
        return model

    def save_model(self, name="model.h5"):
        """
        Save model
        """
        destination = os.path.join("models", name)
        file_name, extension = os.path.splitext(name)

        # save model and weights
        if extension == ".h5":
            self.autoencoder_model.save(destination)
        # save only model
        elif extension == ".json":
            with open(destination, "w") as json_file:
                json.dump(self.autoencoder_model.to_json(), json_file, indent=4)
        elif extension == ".yaml":
            with open(destination, "w") as yaml_file:
                yaml_file.write(self.autoencoder_model.to_yaml())
        else:
            raise TypeError(
                "You can only save models as .h5, .json or .yaml files."
            )

    def _load_model(self, name="model.h5"):
        """
        Load h5 model
        """
        destination = os.path.join("models", name)
        file_name, extension = os.path.splitext(name)

        # load model and weights
        if extension == ".h5":
            return load_model(destination)
        raise TypeError("You can only load '.h5' files.")


if __name__ == "__main__":

    autoencoder = Autoencoder(load_model_name="model.h5")
    print(autoencoder)


class AI(object):
    """docstring for AI."""

    def __init__(self, args, parametres, sorties, experience):
        super(AI, self).__init__()
        # Les arguments de l'experience
        self.args = args
        # Les sorties récupérées de la simulation
        self.sorties = sorties
        # Les résultats récupérés par l'expérience
        self.experience = experience
        # Le modèle d'intelligence artificiel préentrainé
        self.model = None
        # La prévision obtenue par le modèle d'intelligence artificielle
        self.prevision = {}

    def lecture_modele():
        # Récupère le modèle entrainé depuis le fichier modele.skl et le met dans self.model
        pass

    def sauvegarde_modele():
        # Récupère le modèle entrainé dans self.model et le sauvegarde dans le fichier modele.skl
        pass

def arbre_to_image(Arbre) :
    
    