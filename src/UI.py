import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()

#creation de la fenetre
canvas = tk.Canvas(root, height=700, width=700)
canvas.pack()


#creation du frame choix des parametres
frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx = 0.1, rely=0.1)


#creation du titre
titre = tk.Label(frame, text = "Choix des paramètres de la simulation", fg = "white", bg = "green")
titre.pack()


#definition de la fonction qui ouvre les fichiers

def addfichier() :
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("text", "*.text"),("all files", "*./")))



#creation des trois boutons de saisie des parametres
T_ext = tk.Button(frame, text = "Selectionner le fichier de température extérieure", fg="white", bg="gray", command=addfichier)
T_ext.place(relwidth=0.4, relheight=0.1, relx = 0.1, rely=0.2)


T_int = tk.Button(frame, text = "Selectionner le fichier de température intérieure", padx=10, pady=5, fg="white", bg="gray")
T_int.place(relwidth=0.4, relheight=0.1, relx = 0.1, rely=0.4)


Puissance_int = tk.Button(frame, text = "Selectionner le fichier de puissance intérieure", padx=10, pady=5, fg="white", bg="gray")
Puissance_int.place(relwidth=0.4, relheight=0.1, relx = 0.1, rely=0.6)

#creation des trois boutons d'affichage des courbes
T_ext_aff = tk.Button(frame, text = "Afficher la courbe de température extérieure", fg="white", bg="gray")
T_ext_aff.place(relwidth=0.4, relheight=0.1, relx = 0.5, rely=0.2)


T_int_aff = tk.Button(frame, text = "Afficher la courbe de température intérieure", padx=10, pady=5, fg="white", bg="gray")
T_int_aff.place(relwidth=0.4, relheight=0.1, relx = 0.5, rely=0.4)


Puissance_int_aff = tk.Button(frame, text = "Afficher la courbe de puissance intérieure", padx=10, pady=5, fg="white", bg="gray")
Puissance_int_aff.place(relwidth=0.4, relheight=0.1, relx = 0.5, rely=0.6)



















############################
root.mainloop()
