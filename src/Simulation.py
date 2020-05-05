import numpy as np
from scipy.integrate import odeint



class Simulation(object):
    """docstring for Simulation."""

    def __init__(self, grille, args):
        super(Simulation, self).__init__()
        # Contient les arguments de la simulation
        self.args = args
        # Contient la grille qui sert de support à la simulation
        self.grille = grille
        # Continent la sortie de la simulation
        self.sortie = {}
        # Indique si la simulation a fini de tourner ou non
        self.fini = False

# (Litao) Il nous faut initialisation les températures du système
# Idée : Peut-être qu'on pourrait utiliser le Tkinter pour entrer les températures
def initialisationTempetarue(matrice):
    pass

# (Litao) Selons l'équation sur la page 4 du document "mécatroComplementProjet",on enregistre
# les données necéssaires dans une matrice autre que "tableau" pour établir le système d'EDs.
# On néglige pour le moment l'effet des flux thermiques φ.
def initialisationSimulation(tableau):
    [n,m] = np.shape(tableau)
    # n=m, car on a une matrice carrée
    
    nMat = n
    mMat = 3
    matrice = np.zeroes((nMat, mMat))
    # Une matrice qui enregistre les Ci, Hiéquivalent et Ti de chaque maille en ligne(mMat)    
    
    initialisationTemperature(matrice)
    # Initailisation de la température de chaque maille
    
    for i in range(0,n):
        for j in range(0,m):
            if i == j :
                matrice[i][0] = tableau[i][j]
                # le condensateur de chaque maille
            elif tableau[i][j] != 0:
                matrice[i][1] = (matrice[j][2]-matrice[i][2])/tableau[i][j] + matrice[i][1]
                #Calcul de la conductance équivalente
 return matrice

