"""Ce fichier contient la racine de l'interface graphique à laquelle toutes les
pages sont attachées."""

import os  # Utile pour récupérer le dossier courant si besoin
import tkinter as tk

from time import sleep  # Utile pour attendre que la convergence se termine.

from PageLectureDonnees import (
    PageLectureDonnees,
)  # La première page de l'interface
from PageLectureConfiguration import (
    PageLectureConfiguration,
)  # La deuxième page de l'interface
from PageAnimation import (
    PageAnimation,
)  # La troisième page de l'interface graphique


class InterfaceGraphique(tk.Tk):
    """Classe pour l'interface graphique."""

    def __init__(self, dossierCourant=None):
        """Initialisation de la classe."""
        super(InterfaceGraphique, self).__init__()
        # On donne une taille par défaut à notre fenêtre pour qu'elle apparaisse
        # d'une façon plus harmonieuse
        self.geometry("600x600")

        # Le fait de mettre un niveau intermédiaire entre la fenêtre globale
        # (self) et les pages qui vont changer permet de faire des transitions
        # qui semblent subtilement plus fluides.
        self.fenetrePrincipale = tk.Frame(self)
        # On demande à la fenetrePrincipale d'occuper tout l'espace disponible.
        self.fenetrePrincipale.place(relwidth=1, relheight=1)

        if dossierCourant is None:
            # Si le dossier courant n'est pas précisé, on prend le dossier dans
            # lequel le programme est en train de s'exécuter.
            self.dossierCourant = os.getcwd()
        else:
            self.dossierCourant = dossierCourant

        # On commence sur la première page de l'interface
        self.pageCourante = PageLectureDonnees(self)

        # On stocke ici les mesures données par l'utilisateur.
        self.mesures = None

        # On stocke ici les paramètres utiles pour le constructeur de
        # `Genetique`.
        self.constructeur = None

    def afficher(self):
        """Lance l'interface graphique."""
        self.mainloop()

    def pageSuivante(self):
        """Comme son nom l'indique, permet de passer à la page suivante."""
        if type(self.pageCourante) is PageLectureDonnees:
            # On récupère les données de mesure
            self.mesures = (
                self.pageCourante.T,
                self.pageCourante.Tint,
                self.pageCourante.Text,
                self.pageCourante.Pint,
            )
            # On efface ce qui est dans la fenêtre
            self.pageCourante.destroy()
            # On affiche la page suivante
            self.pageCourante = PageLectureConfiguration(self)

        elif type(self.pageCourante) is PageLectureConfiguration:
            # On récupère les paramètres du constructeur de `Genetique`
            self.constructeur = self.pageCourante.valeursConstructeur
            # On efface ce qui est dans la fenêtre
            self.pageCourante.destroy()
            # On affiche la page suivante
            self.pageCourante = PageAnimation(
                self, self.mesures, self.constructeur
            )
            # Il n'y a pas de bouton sur la troisième page, on doit donc passer
            # à la page suivante automatiquement
            self.pageSuivante()

        else:
            # On efface ce qui est dans la fenêtre
            self.pageCourante.destroy()
            # On arrête l'application
            self.destroy()
