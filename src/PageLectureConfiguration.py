"""Implémentation de la page qui sert à récupérer les données de
configuration."""

import tkinter as tk
import json  # Pour lire le fichier de configuration

import intelligenceArtificielle.structureDonnees.Coefficients as Coefficients  # Pour modifier les valeurs globales des coefficients
from intelligenceArtificielle.Genetique import (
    Genetique,  # Pour modifier les paramètres de la classe Génétique
    GenerateurArbres,  # Pour modifier les constantes sur la façon dont les arbres sont créés
)


class PageLectureConfiguration(tk.Frame):
    """Classe pour la page de lecture de la configuration."""

    def __init__(self, interfaceParente):
        super(PageLectureConfiguration, self).__init__(
            interfaceParente.fenetrePrincipale, bg="white"
        )
        self.interfaceParente = interfaceParente
        self.place(relwidth=1, relheight=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # self.place(relx=1, rely=1)

        # Un champ dans lequel on stockera les valeurs pour le constructeur
        # lorsque l'utilisateur les aura confirmées
        self.valeursConstructeur = None

        # On affiche en grille tous les coefficients de la simulation et leurs
        # valeurs.

        # Pour simplifier l'ajout ou la suppression d'une ligne dans le code.
        curseurLigne = 0

        # Le titre de la fenêtre
        self.titre = tk.Label(
            self, text="Configuration de la simulation", fg="white", bg="green"
        )
        self.titre.grid(row=curseurLigne, columnspan=2, sticky=tk.N)
        curseurLigne += 1

        # PREMIERE SECTION : Valeurs pour `Coefficients`
        self.muH, curseurLigne = self.creerLigneConfiguration(
            "muH", Coefficients.muH, curseurLigne
        )
        self.sigH, curseurLigne = self.creerLigneConfiguration(
            "sigH", Coefficients.sigH, curseurLigne
        )
        self.minH, curseurLigne = self.creerLigneConfiguration(
            "minH", Coefficients.minH, curseurLigne
        )
        self.muC, curseurLigne = self.creerLigneConfiguration(
            "muC", Coefficients.muC, curseurLigne
        )
        self.sigC, curseurLigne = self.creerLigneConfiguration(
            "sigC", Coefficients.sigC, curseurLigne
        )
        self.minC, curseurLigne = self.creerLigneConfiguration(
            "minC", Coefficients.minC, curseurLigne
        )
        self.referenceH, curseurLigne = self.creerLigneConfiguration(
            "referenceH", Coefficients.referenceH, curseurLigne
        )
        self.referenceC, curseurLigne = self.creerLigneConfiguration(
            "referenceC", Coefficients.referenceC, curseurLigne
        )
        self.referenceE, curseurLigne = self.creerLigneConfiguration(
            "referenceE", Coefficients.referenceE, curseurLigne
        )

        # DEUXIEME SECTION : Valeurs pour `GenerateurArbres`
        self.profondeurMaxArbre, curseurLigne = self.creerLigneConfiguration(
            "profondeurMaxArbre",
            GenerateurArbres.PROFONDEUR_MAX_ARBRE,
            curseurLigne,
        )
        self.largeurMaxArbre, curseurLigne = self.creerLigneConfiguration(
            "largeurMaxArbre", GenerateurArbres.LARGEUR_MAX_ARBRE, curseurLigne
        )
        self.biaisAlternance, curseurLigne = self.creerLigneConfiguration(
            "biaisAlternance", GenerateurArbres.BIAIS_ALTERNANCE, curseurLigne
        )

        # TROISIEME SECTION : Valeurs pour la classe `Genetique`
        self.chanceDeMutation, curseurLigne = self.creerLigneConfiguration(
            "chanceDeMutation", Genetique.CHANCE_DE_MUTATION, curseurLigne
        )
        (
            self.pourcentageConservationFort,
            curseurLigne,
        ) = self.creerLigneConfiguration(
            "pourcentageConservationFort",
            Genetique.POURCENTAGE_CONSERVATION_FORT,
            curseurLigne,
        )
        self.chanceSurvieFaible, curseurLigne = self.creerLigneConfiguration(
            "chanceSurvieFaible", Genetique.CHANCE_SURVIE_FAIBLE, curseurLigne
        )

        # QUATRIEME SECTION : Valeurs pour le constructeur de `Genetique`
        self.Cint, curseurLigne = self.creerLigneConfiguration(
            "Cint", Coefficients.muC, curseurLigne
        )
        self.taillePopulation, curseurLigne = self.creerLigneConfiguration(
            "taillePopulation", 50, curseurLigne
        )
        self.generationMax, curseurLigne = self.creerLigneConfiguration(
            "generationMax", 25, curseurLigne
        )
        self.objectif, curseurLigne = self.creerLigneConfiguration(
            "objectif", 100, curseurLigne
        )
        self.largeurImage, curseurLigne = self.creerLigneConfiguration(
            "largeurImage", 32, curseurLigne
        )
        self.hauteurImage, curseurLigne = self.creerLigneConfiguration(
            "hauteurImage", 32, curseurLigne
        )
        self.autoencodeur, curseurLigne = self.creerLigneConfiguration(
            "autoencodeur", "base_32x32", curseurLigne
        )

        # DERNIERE SECTION : Le bouton de confirmation
        self.boutonConfirmation = tk.Button(
            self,
            text="Valider la configuration",
            fg="white",
            bg="green",
            command=self.confirmerValeurs,
        )
        self.boutonConfirmation.grid(row=curseurLigne, columnspan=2)

    def creerLigneConfiguration(
        self, nomOption, valeurDefautOption, curseurLigne
    ):
        """Ajoute à l'interface une ligne pour rentrer l'option avec le nom
        passé en argument."""
        # On commence par créer le texte descriptif qui sera à gauche
        nomOption = tk.Label(self, text=nomOption, bg="white")
        # On le place dans l'image
        nomOption.grid(row=curseurLigne, column=0, sticky=tk.W)
        # On crée la zone de texte à remplir à droite
        champOption = tk.Entry(self)
        # On la place sur la fenêtre
        champOption.grid(row=curseurLigne, column=1)
        #
        if type(valeurDefautOption) is float:
            texteValeurOption = notationScienfifique(valeurDefautOption)
        else:
            texteValeurOption = str(valeurDefautOption)
        champOption.insert(0, texteValeurOption)
        curseurLigne += 1
        return champOption, curseurLigne

    def confirmerValeurs(self):
        """Récupère les valeurs dans tous les champs et essaie de les utiliser
        pour la simulation.

        Si un problème de conversion apparait, la valeur par défaut sera gardée.
        A la fin de la méthode, on récupère la liste des valeurs pour le
        constructeur de `Genetique`.
        """

        # PREMIERE SECTION : Valeurs pour `Coefficients`
        Coefficients.muH = float(self.muH.get())
        Coefficients.sigH = float(self.sigH.get())
        Coefficients.minH = float(self.minH.get())
        Coefficients.muC = float(self.muC.get())
        Coefficients.sigC = float(self.sigC.get())
        Coefficients.minC = float(self.minC.get())
        Coefficients.referenceH = float(self.referenceH.get())
        Coefficients.referenceC = float(self.referenceC.get())
        Coefficients.referenceE = float(self.referenceE.get())

        # DEUXIEME SECTION : Valeurs pour `GenerateurArbres`
        GenerateurArbres.PROFONDEUR_MAX_ARBRE = int(
            self.profondeurMaxArbre.get()
        )
        GenerateurArbres.LARGEUR_MAX_ARBRE = int(self.largeurMaxArbre.get())
        GenerateurArbres.BIAIS_ALTERNANCE = float(self.biaisAlternance.get())

        # TROISIEME SECTION : Valeurs pour la classe `Genetique`
        Genetique.CHANCE_DE_MUTATION = float(self.chanceDeMutation.get())
        Genetique.POURCENTAGE_CONSERVATION_FORT = float(
            self.pourcentageConservationFort.get()
        )
        Genetique.CHANCE_SURVIE_FAIBLE = float(self.chanceSurvieFaible.get())

        # QUATRIEME SECTION : Valeurs pour le constructeur de `Genetique`
        self.valeursConstructeur = (
            float(self.Cint.get()),
            int(self.taillePopulation.get()),
            int(self.generationMax.get()),
            float(self.objectif.get()),
            int(self.largeurImage.get()),
            int(self.hauteurImage.get()),
            self.autoencodeur.get(),
        )

        self.interfaceParente.pageSuivante()


def notationScienfifique(nombreFlottant):
    """Renvoie la notation scientifique d'un flottant, utile pour l'affichage
    des valeurs dans l'interface graphique."""
    return "{0:.2E}".format(nombreFlottant)
