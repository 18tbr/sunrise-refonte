import tkinter as tk
import numpy as np
from tkinter import filedialog, Text
import os
import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tk.Tk()

#### OUTILS NUMERIQUES ####

T_ext_valeurs, T_int_valeurs, P_int_valeurs, Temps = [], [], [], []


#### OUTILS GRAPHIQUES ####

#creation de la fenetre
canvas = tk.Canvas(root, height=700, width=700)
canvas.pack()


#creation du frame choix des parametres
frame = tk.Frame(root, bg="white")
frame.place(relwidth=1, relheight=1)


#creation du titre
titre = tk.Label(frame, text = "Choix des paramètres de la simulation", fg = "white", bg = "green")
titre.pack()

#creation du sous titre
titre = tk.Label(frame, text = "1. Saisie des valeurs de température intérieure, température extérieure et puissance intérieure en fonction du temps", fg = "white", bg = "red")
titre.pack()

#definition de la fonction qui ouvre l'explorateur de fichiers
def addfichier1() :
    filename = filedialog.askopenfilename(initialdir="/", title="Sélectionnez le fichier de valeurs", filetypes=(("tableau de valeurs", "*.npy"),("all files", "*./")))
    fichier = open(filename, "r")
    data = np.load(filename)
    if len(data)==2 :
        Temps = data[0]
        T_ext_valeurs = data[1]
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(Temps,T_ext_valeurs)
        canvas = FigureCanvasTkAgg(f, frame)
        canvas.get_tk_widget().place(relwidth=0.7, relheight=0.3, relx = 0.3, rely=0.1)

    else :
        print("Le fichier n'est pas exploitable")

#definition de la fonction qui ouvre l'explorateur de fichiers
def addfichier2() :
    filename = filedialog.askopenfilename(initialdir="/", title="Sélectionnez le fichier de valeurs", filetypes=(("tableau de valeurs", "*.npy"),("all files", "*./")))
    fichier = open(filename, "r")
    data = np.load(filename)
    if len(data)==2 :
        Temps = data[0]
        T_int_valeurs = data[1]
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(Temps,T_int_valeurs)
        canvas = FigureCanvasTkAgg(f, frame)
        canvas.get_tk_widget().place(relwidth=0.7, relheight=0.3, relx = 0.3, rely=0.4)

    else :
        print("Le fichier n'est pas exploitable")

def addfichier3() :
    filename = filedialog.askopenfilename(initialdir="/", title="Sélectionnez le fichier de valeurs", filetypes=(("tableau de valeurs", "*.npy"),("all files", "*./")))
    fichier = open(filename, "r")
    data = np.load(filename)
    if len(data)==2 :
        Temps = data[0]
        P_int_valeurs = data[1]
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(Temps,P_int_valeurs)
        canvas = FigureCanvasTkAgg(f, frame)
        canvas.get_tk_widget().place(relwidth=0.7, relheight=0.3, relx = 0.3, rely=0.7)

    else :
        print("Le fichier n'est pas exploitable")


#creation des trois boutons de saisie des parametres
# ------> quand on ouvre un fichier, il s'affiche automatiquement à côté


T_ext = tk.Button(frame, text = "Température extérieure", fg="white", bg="gray", command=addfichier1)
T_ext.place(relwidth=0.2, relheight=0.1, relx = 0.1, rely=0.2)


T_int = tk.Button(frame, text = "Température intérieure", padx=10, pady=5, fg="white", bg="gray", command=addfichier2)
T_int.place(relwidth=0.2, relheight=0.1, relx = 0.1, rely=0.5)


P_int = tk.Button(frame, text = "Puissance intérieure", padx=10, pady=5, fg="white", bg="gray", command=addfichier3)
P_int.place(relwidth=0.2, relheight=0.1, relx = 0.1, rely=0.8)
















############################
root.mainloop()
