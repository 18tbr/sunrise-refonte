# Ce fichier contient l'implémentation de la page de récupération des courbes de l'utilisateur.

import tkinter as tk
import numpy as np  # Utile pour lire les fichiers npy
import matplotlib   # Utile pour tracer les courbes

# from matplotlib import style
# from tkinter import filedialog, Text

# Configuration de matplotlib pour pouvoir intégrer les courbes dans l'interface graphique.
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Outils import lireTableau  # Utile pour récupérer les mesures contenues dans un fichier.
from SunRiseException import FichierIncoherent  # Lancée lorsque les différentes bases de temps des fichiers ne sont pas les mêmes

class PageLectureDonnees(tk.Frame):
    """docstring for PageLectureDonnees."""

    def __init__(self, interfaceParente):
        super(PageLectureDonnees, self).__init__(interfaceParente.fenetrePrincipale, bg='white')
        self.interfaceParente = interfaceParente
        self.place(relwidth=1, relheight=1)

        # Les conteneurs de T, Tint, Text et Pint qui permettront de récupérer les valeurs une fois que l'utilisateur les aura rentrées
        self.T = None
        self.Tint = None
        self.Text = None
        self.Pint = None

        # Le titre de la fenêtre
        self.titre = tk.Label(self, text="Choix des données de mesure", fg="white", bg="green")
        self.titre.pack()

        # Le bouton pour choisir la température intérieure
        self.boutonTint = tk.Button(
            self,
            text="Tint",
            padx=10,
            pady=5,
            fg="white",
            bg="gray",
            command=self.ajoutFichierTint,
        )
        self.boutonTint.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.2)

        # Le bouton pout la tempérautre extérieure
        self.boutonText = tk.Button(
            self,
            text="Text",
            fg="white",
            bg="gray",
            command=self.ajoutFichierText,
        )
        self.boutonText.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.5)

        self.boutonPint = tk.Button(
            self,
            text="Pint",
            padx=10,
            pady=5,
            fg="white",
            bg="gray",
            command=self.ajoutFichierPint,
        )
        self.boutonPint.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.8)

        self.boutonConfirmation = tk.Button(
            self,
            text="Confirmer les mesures",
            fg="white",
            bg="green",
            command=self.confirmerValeurs,
        )
        self.boutonConfirmation.pack(side=tk.BOTTOM)

    # Les alias de la fonction ajoutFichier avec les bons arguments pour les boutons.
    def ajoutFichierTint(self):
        self.ajoutFichier(self.Tint, 0.1)

    def ajoutFichierText(self):
        self.ajoutFichier(self.Text, 0.4)

    def ajoutFichierPint(self):
        self.ajoutFichier(self.Pint, 0.7)

    def ajoutFichier(self, conteneur, hauteurRelative):
        # hauteurRelative désigne la hauteur du graphe qui sera tracé et conteneur est soit Tint, soit Text, soit Pint et sert à contenir les valeurs recues. figure est la figure sur laquelle on doit tracer notre courbe.
        nomFichier = tk.filedialog.askopenfilename(
            initialdir=self.interfaceParente.dossierCourant,
            title="Sélectionnez le fichier de valeurs",
            filetypes=(("tableau csv", "*.csv"), ("tableau numpy", "*.npy"), ("all files", "*./")),
        )

        # On transpose les valeurs recues pour pouvoir les séparer plus facilement
        T, grandeur = lireTableau(nomFichier).T

        if self.T is None:
            # Si on n'a pas encore de valeur pour T, on la récupère du fichier
            self.T = T
        elif (self.T != T).any():
            # Les données sont incohérentes, on a un problème avec la base de temps.
            raise FichierIncoherent(f"Les données dans le fichier {nomFichier} n'ont pas la même base de temps que celles présentes dans un autre fichier enregistré plus tôt.")
        # Sinon tout va bien

        # On stocke la grandeur dans le conteneur passé en argument. On modifie le conteneur par effet de bord en évitant de le remplacer par une variable locale
        conteneur = grandeur

        # On remplit la figure que l'on va afficher sur l'interface. On commence par créer la figure qui va contenir la courbe.
        figure = Figure(figsize=(5, 5), dpi=100)

        # On créé une nouvelle courbe
        courbe = figure.add_subplot(111)
        # Enfin on trace la courbe
        courbe.plot(self.T, conteneur)

        # Il ne reste plus qu'à afficher le résultat dans un canevas dédié
        canevasCourbe = FigureCanvasTkAgg(figure, self)
        canevasCourbe.get_tk_widget().place(
                relwidth=0.7, relheight=0.3, relx=0.3, rely=hauteurRelative
        )

    def confirmerValeurs(self):
        self.interfaceParente.pageSuivante()
