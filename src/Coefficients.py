# Ce module contient les valeurs des coefficients utilisés. Il est utilisé pour générer des coefficients aléatoires de façon cohérent ou étalonner certaines valeurs.

from random import (
    gauss,
)  # Loi gaussienne utilisée pour générer des coefficients aléatoires

# Note : les valeurs définies ci dessous sont accessibles de l'exterieur comme Coefficients.<nom> dans les autres modules où Coefficeints est importé.

# IMPORTANT : En pratique, les équations différentielles ne sont solubles que si C >> H, (il faut 1 à 2 ordres de grandeur de différence). La raison est, il me semble, que le temps caractéristique de l'équation ne doit pas être plus petit que le temps de discrétisation par le solveur. Notez également que le solveur met significativement plus de temps à traiter les équations en cas de problèmes que s'il n'y en a pas.

# Ces valeurs donnent la loi des coefficients de transmission H
muH = 5e-1  # Valeur moyenne
sigH = 10e-1  # Ecart type
minH = 1e-1  # Valeur minimale (> 0)

# Fonction de génération de conductances aléatoires
def conductance():
    return max(gauss(muH, sigH), minH)


# Ces valeurs donnent la loi des coefficients de capacités C
muC = 5e1  # Valeur moyenne
sigC = 10e1  # Ecart type
minC = 1e1  # Valeur minimale (> 0)

# Bien régler les valeurs minimales pour même dans le pire des cas on conserve deux ordres de grandeur de différence entre C et H accélère sensiblement l'algorithme.

# Fonction de génération de capacités aléatoires
def capacite():
    return max(gauss(muC, sigC), minC)


referenceH = muH + 5 * sigH
referenceC = muC + 5 * sigC
referenceE = 100
