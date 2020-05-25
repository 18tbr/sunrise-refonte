# L'implémentation de la troisième page de l'interface graphique

import numpy as np  # Utile pour estimer la taille à donner à la fenêtre de l'animation.
import tkinter as tk
import tkinter.ttk as ttk  # Contient le widget pour les barres de progression.
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# Configuration de matplotlib pour pouvoir intégrer les courbes dans l'interface graphique.
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Genetique import (
    Genetique,
    GenerateurArbres,
)  # On va réaliser l'algorithme génétique dans cette page.


class PageAnimation(tk.Frame):
    """docstring for PageAnimation."""

    def __init__(self, interfaceParente, donneesMesures, argumentsConstructeur):
        super(PageAnimation, self).__init__(
            interfaceParente.fenetrePrincipale, bg="white"
        )
        self.interfaceParente = interfaceParente
        self.place(relwidth=1, relheight=1)

        # On commence par initialiser l'objet Génétique qui va servir à faire l'algorithme.On commence par mettre certaines variables globales aux bonnes valeurs.
        Genetique.SILENCE = True
        GenerateurArbres.SILENCE = True

        # On récupère les données de mesure.
        T, Tint, Text, Pint = donneesMesures

        # On récupère les paramètres du constructeur
        (
            Cint,
            taillePopulation,
            generationMax,
            objectif,
            self.imageLargeur,
            self.imageHauteur,
            autoencodeur,
        ) = argumentsConstructeur

        # On initialise notre objet Génétique en mode graphique
        self.evolution = Genetique(
            Cint,
            T,
            Text,
            Tint,
            Pint,
            taillePopulation,
            generationMax,
            objectif,
            self.imageLargeur,
            self.imageHauteur,
            autoencodeur,
            modeGraphique=True,
        )

        # On donne un titre à notre page
        self.titrePage = tk.Label(
            self, text="Réalisation de la simulation", fg="white", bg="green"
        )
        self.titrePage.pack()

        # On donne une information sur la barre de progression
        self.explicationBarre = tk.Label(
            self, text="Progression de l'initialisation", fg="black", bg="white"
        )
        self.explicationBarre.pack(pady=10)

        # On crée une barre de progression qui servira à suivre la progression de l'initialisation.
        self.barreProgressionInitialisation = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=100, mode="determinate"
        )
        self.barreProgressionInitialisation.pack(
            expand=True, fill="both", padx=10, pady=10
        )

        # On créé la figure qui contiendra l'animation principale de progression de l'algorithme.
        self.figureAnimee = Figure(figsize=(5, 5), dpi=100)
        self.figureAnimee.subplots_adjust(hspace=0.5)

        # On fixe à l'avance les limites de l'animation.
        limitesAbscisse = (0, generationMax)
        limitesOrdonnee = (estimationLimitesGraphe(Tint), 0)

        # On créé deux nouvelles courbes : une pour la progression de la convergence et une pour l'image du meilleur individu
        self.courbeAnimee = self.figureAnimee.add_subplot(
            211, xlim=limitesAbscisse, ylim=limitesOrdonnee
        )
        self.courbeAnimee.set_title("Convergence de l'algorithme")

        # On fixe à l'avance les axes pour les deux images
        self.imageMeilleur = self.figureAnimee.add_subplot(
            212,
            xlim=(0, self.imageHauteur - 1),
            ylim=(0, self.imageLargeur - 1),
        )
        self.imageMeilleur.set_title("Meilleur individu")

        # Les conteneurs des abscisses et ordonnées des points de l'animation
        self.X, self.Y = [], []
        (self.ligne,) = self.courbeAnimee.plot(self.X, self.Y)

        # De même, on trace le graphe pour les images
        self.matrice = np.zeros((self.imageHauteur, self.imageLargeur))
        self.image = self.imageMeilleur.imshow(self.matrice)

        # Il ne reste plus qu'à afficher le résultat dans un canevas dédié
        canevasCourbe = FigureCanvasTkAgg(self.figureAnimee, self)
        canevasCourbe.get_tk_widget().pack(side=tk.BOTTOM)

        # On initialise la population en utilisant la méthode dédiée populationAleatoireAnimee
        generateurAnimeInitialisation = (
            self.evolution.generateur.populationAleatoireAnimee()
        )
        # Tant que l'itérateur produit des valeurs.
        while True:
            try:
                self.barreProgressionInitialisation["value"] = next(
                    generateurAnimeInitialisation
                )
                self.update_idletasks()
            except StopIteration:
                # On a fini d'initialiser notre population, le générateur est épuisé.
                self.barreProgressionInitialisation["value"] = 100
                break

        # On lance ensuite l'algorithme d'optimisation
        self.generateurOptimisation = self.evolution.optimisation()
        #
        # # L'animation principale
        # animationPrincipale = anim.FuncAnimation(
        #     self.figureAnimee,
        #     self.fonctionAnimation,
        #     frames=self.evolution.optimisation,
        #     blit=True,
        #     repeat=False
        # )

        while True:
            try:
                argumentAnimation = next(self.generateurOptimisation)
                self.fonctionAnimation(argumentAnimation)
                # Ici on force les courbes à être retracées sur le thread principal au lieu du thread de l'interface, ce qui n'est pas une très bonne solution, mais je ne vois pas trop comment faire autrement.
                canevasCourbe.draw()
            except StopIteration:
                break

    def fonctionAnimation(self, argumentsAlgorithmeGenetique):
        (
            generation,
            meilleurIndividu,
            meilleurScore,
        ) = argumentsAlgorithmeGenetique
        print(generation)
        self.X.append(generation)
        self.Y.append(meilleurScore)
        self.matrice = meilleurIndividu.ecritureImage(
            largeur=self.imageLargeur, hauteur=self.imageHauteur
        )
        self.ligne.set_data(self.X, self.Y)
        self.image.set_data(self.matrice)
        return self.ligne, self.image


def estimationLimitesGraphe(Tint):
    # Fonction utilisée pour estimer les limites à donner au graphe utilisé pour l'animation
    return -3 * np.mean(np.square(Tint), 0)