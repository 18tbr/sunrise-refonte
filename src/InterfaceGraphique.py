# Ce fichier contient la racine de l'interface graphique à laquelle toutes les pages sont attachées

import os   # Utile pour récupérer le dossier courant si besoin
import tkinter as tk

from PageLectureDonnees import PageLectureDonnees   # La première page de l'interface
from PageLectureConfiguration import PageLectureConfiguration   # La deuxième page de l'interface

class InterfaceGraphique(tk.Tk):
    """docstring for InterfaceGraphique."""

    def __init__(self, dossierCourant=None):
        super(InterfaceGraphique, self).__init__()
        # On donne une taille par défaut à notre fenêtre pour qu'elle apparaisse d'une façon plus harmonieuse
        self.geometry("550x550")

        # Le fait de mettre un niveau intermédiaire entre la fenêtre globale (self) et les pages qui vont changer permet de faire des transitions qui semblent subtilement plus fluides.
        self.fenetrePrincipale = tk.Frame(self)
        # On demande à la fenetrePrincipale d'occuper tout l'espace disponible.
        self.fenetrePrincipale.place(relwidth=1, relheight=1)

        if dossierCourant is None:
            # Si le dossier courant n'est pas précisé, on prend le dossier dans lequel le programme est en train de s'exécuter.
            self.dossierCourant = os.getcwd()
        else:
            self.dossierCourant = dossierCourant

        # On commence sur la première page de l'interface
        self.pageCourante = PageLectureDonnees(self)

        # On va stocker les mesures données par l'utilisateur ici.
        self.mesures = None

        # On stockera ici les paramètres utiles pour le constructeur de Genetique
        self.constructeur = None

    def afficher(self):
        # La fonction qui lance l'interface graphique.
        self.mainloop()

    def pageSuivante(self):
        # Fonction qui, comme son nom l'indique, permet de passer à la page suivante.
        if type(self.pageCourante) is PageLectureDonnees:
            # On efface ce qui est dans la fenêtre
            self.pageCourante.destroy()
            # On lui rend un taille nécessaire pour contenir ce qui va suivre.
            self.geometry("550x550")
            # On affiche la page suivante
            self.pageCourante = PageLectureConfiguration(self)
        elif type(self.pageCourante) is PageLectureConfiguration:
            # On efface ce qui est dans la fenêtre
            self.pageCourante.destroy()
            # On arrête l'application
            self.destroy()
