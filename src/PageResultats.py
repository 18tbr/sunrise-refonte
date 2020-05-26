"""Implémentation de la quatrième page de l'interface graphique qui affiche les courbes à l'utilisateur."""
import tkinter as tk
import numpy as np  # Utile pour lire les fichiers npy
import matplotlib  # Utile pour tracer les courbes

# Configuration de matplotlib pour pouvoir intégrer les courbes dans l'interface
# graphique.
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PageResultats(tk.Frame):
    """Classe pour la page d'affichage des résultats'."""

    def __init__(
        self, interfaceParente, populationRecuperee, meilleurIndividu, T, Tint
    ):
        """Initialisation de la classe."""
        super(PageResultats, self).__init__(
            interfaceParente.fenetrePrincipale, bg="white"
        )
        self.interfaceParente = interfaceParente
        self.place(relwidth=1, relheight=1)

        # On donne un titre à notre page
        self.titrePage = tk.Label(
            self, text="Résultats de l'optimisation", fg="white", bg="green"
        )
        self.titrePage.pack()

        self.population = populationRecuperee
        self.meilleurIndividu = meilleurIndividu

        # On calcule le score de tous les individus de la population et on les trie pour faire un bel affichage
        self.scores = sorted([arbre.score() for arbre in self.population])

        TintCalculee = self.meilleurIndividu.simulation().y[0]

        # On commence par créer la figure qui va contenir les courbes.
        self.figureResultats = Figure(figsize=(5, 5), dpi=100)
        self.figureResultats.subplots_adjust(hspace=0.5)

        # On remplit la première courbe pour afficher le Tint de référence et le Tint
        courbeTemperatures = self.figureResultats.add_subplot(211)
        (reference,) = courbeTemperatures.plot(T, Tint, "g")
        (calcul,) = courbeTemperatures.plot(T, TintCalculee, "r")
        courbeTemperatures.legend([reference, calcul], ["Mesure", "Simulation"])
        courbeTemperatures.set_title(
            "Comparaison du Tint obtenu par mesure et par le meilleur individu"
        )

        # On remplit la seconde courbe pour afficher les erreurs dans la population globale
        courbeErreurs = self.figureResultats.add_subplot(212)
        courbeErreurs.plot(range(len(self.scores)), self.scores)
        courbeErreurs.set_title("Graphe de l'erreur dans la population")

        # Il ne reste plus qu'à afficher le résultat dans un canevas dédié
        canevasCourbe = FigureCanvasTkAgg(self.figureResultats, self)
        canevasCourbe.get_tk_widget().pack(fill="both", expand=True)
