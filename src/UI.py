# (TBR) Explique à côté de chaque import à quoi il sert dans le code (en un mot). Par exemple pour numpy tu pourrais dire "utile pour lire les fichier .npy"
import tkinter as tk
import numpy as np
from tkinter import filedialog, Text
import os
import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# (TBR) Vu que l'interface graphique est le "main" de notre travail, vous pouvez la garder en style impératif sans trop de problèmes.

racineInterface = tk.Tk()

#### OUTILS NUMERIQUES ####

valeursText, valeursTint, valeursPint, Temps = [], [], [], []


#### OUTILS GRAPHIQUES ####

#creation de la fenêtre
fenetrePrincipale = tk.Canvas(racineInterface, height=700, width=700)
fenetrePrincipale.pack()


#creation de la vue de choix des parametres
vueChoixParametres = tk.Frame(racineInterface, bg="white")
vueChoixParametres.place(relwidth=1, relheight=1)


#creation du titre
titre = tk.Label(vueChoixParametres, text = "Choix des paramètres de la simulation", fg = "white", bg = "green")
titre.pack()

#creation du sous titre
titre = tk.Label(vueChoixParametres, text = "1. Saisie des valeurs de température intérieure, température extérieure et puissance intérieure en fonction du temps", fg = "white", bg = "red")
titre.pack()

#definition de la fonction qui ouvre l'explorateur de fichiers
def ajoutFichier1() :
    nomFichier = filedialog.askopennomFichier(initialdir="/", title="Sélectionnez le fichier de valeurs", filetypes=(("tableau de valeurs", "*.npy"),("all files", "*./")))
    # (TBR) La syntaxe correcte pour ouvrir des fichiers est celle du with, l'ouvrir directement avec fichier = open est source de bug (notamment si on oublie de mettre le close associé).
    with open(nomFichier, "r") as fichier:
        donnees = np.load(nomFichier)
        if len(donnees)==2 :
            Temps = donnees[0]
            valeursText = donnees[1]
            f = Figure(figsize=(5,5), dpi=100)
            a = f.add_subplot(111)
            a.plot(Temps,valeursText)
            fenetrePrincipale = FigureCanvasTkAgg(f, vueChoixParametres)
            fenetrePrincipale.get_tk_widget().place(relwidth=0.7, relheight=0.3, relx = 0.3, rely=0.1)

        else :
            print("Le fichier n'est pas exploitable")

#definition de la fonction qui ouvre l'explorateur de fichiers
def ajoutFichier2() :
    nomFichier = filedialog.askopennomFichier(initialdir="/", title="Sélectionnez le fichier de valeurs", filetypes=(("tableau de valeurs", "*.npy"),("all files", "*./")))
    with open(nomFichier, "r") as fichier:  # cf ajoutFichier1
        donnees = np.load(nomFichier)
        if len(donnees)==2 :
            Temps = donnees[0]
            valeursTint = donnees[1]
            f = Figure(figsize=(5,5), dpi=100)
            a = f.add_subplot(111)
            a.plot(Temps,valeursTint)
            fenetrePrincipale = FigureCanvasTkAgg(f, vueChoixParametres)
            fenetrePrincipale.get_tk_widget().place(relwidth=0.7, relheight=0.3, relx = 0.3, rely=0.4)

        else :
            print("Le fichier n'est pas exploitable")

def ajoutFichier3() :
    nomFichier = filedialog.askopennomFichier(initialdir="/", title="Sélectionnez le fichier de valeurs", filetypes=(("tableau de valeurs", "*.npy"),("all files", "*./")))
    with open(nomFichier, "r") as fichier:  # cf ajoutFichier1
        donnees = np.load(nomFichier)
        if len(donnees)==2 :
            Temps = donnees[0]
            valeursPint = donnees[1]
            f = Figure(figsize=(5,5), dpi=100)
            a = f.add_subplot(111)
            a.plot(Temps,valeursPint)
            fenetrePrincipale = FigureCanvasTkAgg(f, vueChoixParametres)
            fenetrePrincipale.get_tk_widget().place(relwidth=0.7, relheight=0.3, relx = 0.3, rely=0.7)

        else :
            print("Le fichier n'est pas exploitable")


#creation des trois boutons de saisie des parametres
# ------> quand on ouvre un fichier, il s'affiche automatiquement à côté


boutonText = tk.Button(vueChoixParametres, text = "Température extérieure", fg="white", bg="gray", command=ajoutFichier1)
boutonText.place(relwidth=0.2, relheight=0.1, relx = 0.1, rely=0.2)


boutonTint = tk.Button(vueChoixParametres, text = "Température intérieure", padx=10, pady=5, fg="white", bg="gray", command=ajoutFichier2)
boutonTint.place(relwidth=0.2, relheight=0.1, relx = 0.1, rely=0.5)


boutonPint = tk.Button(vueChoixParametres, text = "Puissance intérieure", padx=10, pady=5, fg="white", bg="gray", command=ajoutFichier3)
boutonPint.place(relwidth=0.2, relheight=0.1, relx = 0.1, rely=0.8)


# (TBR) Quelques remarques :
# (TBR) Si vous voulez que votre interface fonctionne bien, il faut que vous utilisiez une disposition (grid layout est probablement ce que vous voulez ici), sinon l'interface va casser sur un PC avec un écran d'une taille différente ou lorsque la fenètre chage de taille.
# (TBR) Coder trois fois la même fonction avec juste une petite différente de placement n'est pas une bonne façon de régler le problème. Une solution aussi simple serait d'utiliser une lambda fonction : vous commencer par écrire ajoutFichier qui prend rely en paramètre, puis dans chaque bouton vous remplcez ajoutFichierX par (lambda: ajoutFichier(X)) qui est une lambda fonction qui fait ce que vous voulez. Ce n'est qu'une seule solution parmi d'autres mais je pense que c'est ce que vous voulez ici.


############################
racineInterface.mainloop()
