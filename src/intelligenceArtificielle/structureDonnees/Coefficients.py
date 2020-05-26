"""Ce module contient les valeurs des coefficients utilisés.
Il est utilisé pour générer des coefficients aléatoires de façon cohérente ou
étalonner certaines valeurs.

Note : les valeurs définies ci dessous sont accessibles de l'extérieur comme
Coefficients.<nom> dans les autres modules où Coefficients est importé.

IMPORTANT
---------
En pratique, les équations différentielles ne sont solubles que si C >> H, (il
faut 1 à 2 ordres de grandeur de différence) pour un pas de temps de 1.
La raison est, il me semble, que le temps caractéristique de l'équation ne doit
pas être plus petit que le temps de discrétisation par le solveur. Notez
également que le solveur met significativement plus de temps à traiter les
équations en cas de problèmes que s'il n'y en a pas.
"""

from random import (
    gauss,
)  # Loi gaussienne utilisée pour générer des coefficients aléatoires


# Ces valeurs donnent la loi des coefficients de transmission H
muH = 5e-2  # Valeur moyenne
sigH = 10 * muH  # Ecart type
minH = 1e-2  # Valeur minimale (> 0)

# Fonction de génération de conductances aléatoires
def conductance():
    return max(gauss(muH, sigH), minH)


# Ces valeurs donnent la loi des coefficients de capacités C
muC = 5e6  # Valeur moyenne
sigC = 10 * muC  # Ecart type
minC = 1e6  # Valeur minimale (> 0)

# Bien régler les valeurs minimales pour que même dans le pire des cas on
# conserve deux ordres de grandeur de différence entre C et H accélère
# sensiblement l'algorithme.

# Fonction de génération de capacités aléatoires
def capacite():
    return max(gauss(muC, sigC), minC)


# Le "/10" dans ce qui suit vient du fait que sigmoid(1) ~= 0.7, donc pour avoir
# des couleurs bien étalées afin de rendre l'image plus imitable pour le réseau
# de neurones, il faut prendre une référence 10x plus petite (sigmoid(10) ~= 1).
referenceH = (muH + 5 * sigH) / 10
referenceC = (muC + 5 * sigC) / 10
referenceE = 100 / 10
