import numpy as np
from random import randint
from scipy.integrate import (
    solve_ivp,
)  # Version moderne et orienté objet de odeint
from scipy.interpolate import (
    interp1d,
)  # Interpolation par spline utilisée pour la résolution d'équation différentielle
from scipy.special import (
    expit,
)  # Une implémentation de la fonction sigmoïde utilisée pour la propagation d'erreur.
import GrilleUtils
from Noeuds import Feuille, Parallele, Serie, Noeud


class Grille(object):
    """docstring for Grille."""

    def __init__(self, cint, T, Text, Tint, Pint):
        super(Grille, self).__init__()
        # Capacité thermique associée à l'air intérieur
        self.cint = cint
        # Nombre de condensateurs dans le réseau, il doit au moins y avoir cint
        self.nbCondensateurs = 1
        # La forme du réseau, résumée au nombre de noeuds à chaque profondeur
        self.forme = [0]  # Sera passé à 1 par le constructeur de Feuille
        # La liste des temps (pour Text, Tint, Pint)
        self.T = T
        # La série des températures extérieures
        if T is not None and Text is not None:
            # Pour résoudre l'équation différentielle on a besoin d'une interpolation de la température au cours du temps.
            self.Text = interp1d(T, Text, kind="linear")
        else:
            # Notez que le fait de passer None en argument doit être traduit par une fonction pour que le code fonctionne, mais ne donnera jamais des résultats de simulation correcte. On autorise ce comportement de façon temporaire pour simplifier certains tests.
            self.Text = lambda t: 0
        # La série des températures intérieures
        self.Tint = Tint
        # La série des puissances intérieures
        if T is not None and Pint is not None:
            self.Pint = interp1d(T, Pint, kind="linear")
        else:
            self.Pint = lambda t: 0
        # IMPORTANT : ne pas ajouter une feuille avant d'avoir défini la forme de la grille
        # La racine de l'arbre
        self.racine = Feuille(self)

    def creationSimulation(self):
        nbTemperatures = self.nbCondensateurs
        # L'équation différentielle à résoudre sera :
        # C^-1 dT/dt = AT + BQ
        # Pour la signification de chacune de ces matrices, voire les fonctions de résolution de l'équation différentielle.
        A = np.zeros((nbTemperatures, nbTemperatures))
        B = np.zeros((nbTemperatures, 2))
        C = np.eye(nbTemperatures)
        C[0, 0] /= self.cint  # La capacité sur Tint n'est pas dans l'arbre
        result, curseur = self.racine.creationSimulationRecursive(
            A, B, C, gauche=None, droite=0, curseur=0
        )
        # Il reste à rentrer dans le tableau la valeur du lien entre Tint et Text
        if result is not None:
            A[0, 0] += result
            B[0, 0] = -result
        B[
            0, 1
        ] = 1  # La puissance intérieure s'applique sur Tint, indépendamment de si la racine est une liaison série ou non.
        # On crée récursivement le tableau en partant de la racine.
        return A, B, C

    def creationMarquage(self):
        # Le début de la fonction de marquage est très proche de celui de creationSimulation
        nbTemperatures = self.nbCondensateurs
        A = np.zeros((nbTemperatures, nbTemperatures))
        B = np.zeros((nbTemperatures, 2))
        C = np.eye(nbTemperatures)
        C[0, 0] /= self.cint  # La capacité sur Tint n'est pas dans l'arbre
        # D est la matrice des délais dans le réseau RC
        D = np.zeros((nbTemperatures + 1, nbTemperatures + 1))
        delai, result, curseur = self.racine.creationMarquageRecursif(
            A,
            B,
            C,
            D,
            gauche=None,
            droite=0,
            curseur=0,
            conteneur=None,
            capaciteDroite=self.cint,
        )

        # Il reste à rentrer dans le tableau la valeur du lien entre Tint et Text comme dans creationSimulation
        if result is not None:
            A[0, 0] += result
            B[0, 0] = -result
        B[0, 1] = 1

        # Note importante : il est inutile de finir le travail sur D avec le lien entre Tint et Text car nous n'aurons pas à propager l'erreur sur Text. On renvoie enfin ce que l'on a obtenue. Notez que l'on ne renvoie pas la première ligne et la première colonne de D, qui concernent Text et ne seront qu'encombrantes ensuite.
        return A, B, C, D[1:, 1:], delai

    def simulation(self):
        A, B, C = self.creationSimulation()
        # Résoudre C^-1 dT/dt = AT + BQ
        nbTemperatures = self.nbCondensateurs
        # Hypothèse : Au début de la simulation, tout est à l'équilibre à la température extérieure Text(t=0)
        T0 = np.full((nbTemperatures), self.Text(0))

        def gradient(t, T):
            # dT/dt = gradient(T,t) = C * (AT + BQ)
            # Notez que self.Text et self.Pint sont des interpolations par spline des Text et Pint passés en argument à l'origine.
            return C @ (A @ T + B @ np.array([[self.Text(t)], [self.Pint(t)]]))

        # Attention à la façon dont solve_ivp fonctionne et en particulier à t_span et t_eval (qui sont différents d'odeint si ma mémoire est bonne).
        return solve_ivp(
            fun=gradient,
            t_span=(self.T[0], self.T[-1]),
            y0=T0,
            method="RK45",
            t_eval=self.T,
            vectorized=True,
        )

    def propagationErreur(self):
        # Le début de l'implémentation de cette fonction est très proche de simulation.
        A, B, C, D, delay = self.creationMarquage()
        # Le détail du calcul de simulation effectué ici est documenté dans la méthode simulation
        nbTemperatures = self.nbCondensateurs
        T0 = np.full((nbTemperatures), self.Text(0))

        def gradient(t, T):
            # dT/dt = gradient(T,t) = C * (AT + BQ)
            # Notez que self.Text et self.Pint sont des interpolations par spline des Text et Pint passés en argument à l'origine.
            return C @ (A @ T + B @ np.array([[self.Text(t)], [self.Pint(t)]]))

        # Attention à la façon dont solve_ivp fonctionne et en particulier à t_span et t_eval (qui sont différents d'odeint si ma mémoire est bonne).
        calcul = solve_ivp(
            fun=gradient,
            t_span=(self.T[0], self.T[-1]),
            y0=T0,
            method="RK45",
            t_eval=self.T,
            vectorized=True,
        )

        calculTint = calcul.y[0]
        ecart = self.Tint - calculTint
        # On calcule maintenant l'intégrale de l'erreur pour Tint sur toute la simulation
        epsilon = np.sum(ecart, 0)

        # np.vectorize sert à créer une fonction vectorisée simplement
        sig = np.vectorize(lambda t: int(255 * expit(t / 100)), otypes=[int])
        # Fonction de pénalité de proximité temporelle
        pi = lambda t: 1 / (1 + t / delay)

        # On alloue le vecteur des erreurs propagées
        E = np.array([0 for i in range(nbTemperatures)])

        # On initialise en notant l'erreur associée à Tint que l'on va essayer de propager.
        E[0] = epsilon
        # La file qui nous permet de traiter de façon cohérente toutes le températures
        fileTraitementTempérature = [0]
        for i in range(nbTemperatures):
            if E.all():
                # Si jamais on a alloué une erreur à toutes les températures internes, on peut
                break
            else:
                # On traite la première température possible
                t = fileTraitementTempérature[i]
                for j in range(nbTemperatures):
                    if E[j] == 0:  # Sinon la température a déjà été atteinte
                        delayIJ = D[i, j]
                        if delayIJ != 0:
                            # Formule de rétropropagation heuristique de l'erreur
                            E[j] = E[i] * pi(delayIJ)
                            fileTraitementTempérature.append(j)

        # On renvoie le vecteur de valeurs (entre 0 et 255) pour la pénalité de chaque couleur sur l'image
        return sig(E)

    def score(self):
        # On calcule toutes le températures internes au fil du temps
        calcul = self.simulation()
        # On récupère la température intérieure (la première dans la matrice). Attention, la façon dont solve_ivp restitue les températures n'est pas la même que pour odeint.
        calculTint = calcul.y[0]
        # On calcule l'écart entre la température calculée et la référence
        ecart = self.Tint - calculTint
        # On renvoie l'opposé de l'écart quadratique cumulé. Comme cela plus le score est grand, plus l'arbre est bon, ce qui est plus intuitif pour l'algorithme génétique.
        return -np.sum(np.square(ecart), 0)

    # Utilise la rétropropagation d'erreurs heuristiques dans l'arbre pour marquer les trois couleurs sur chaque noeud.
    def marquage(self):
        E = self.propagationErreur()
        self.racine.injectionMarquage(
            E, gauche=None, droite=0, curseur=0, capaciteDroite=self.cint
        )

    # Effectue un parcours en profondeur de l'arbre sous la racine jusqu'à atteindre le index ième noeud à la profondeur donnée. Renvoie le noeud trouvé.
    def inspecter(self, profondeur, index):
        if profondeur >= len(self.forme):
            raise IndexError(
                f"La profondeur de l'arbre désigné est {len(self.forme)}, il n'y a donc pas de noeuds à la profondeur {profondeur}."
            )
        # else...

        file = [self.racine]
        filePrecedente = [self.racine]
        profondeurParcours = 0
        while profondeurParcours < profondeur:
            file = []
            for noeudChoisi in filePrecedente:
                # Concatenation de liste
                file += noeudChoisi.fils
            profondeurParcours += 1
            filePrecedente = file

        if index >= len(file):
            raise IndexError(
                f"Il n'y a que {len(file)} noeuds à la profondeur {profondeur} de cette arbre, vous ne pouvez donc pas en récupérer le {index}ième."
            )
        # else...

        return file[index]

    def ecritureImage(self, dimImage=(100, 100, 3)):
        """
        Convertit un arbre en image.

        Parameters
        ----------
        dimImage : (int, int, int)
            Taille de l'image souhaitée (hauteur, largeur, profondeur).
        """
        image = np.zeros(dimImage)
        GrilleUtils.creerImage(
            racine=self.racine,
            numRacine=0,
            coinHautGauche=(0, 0),
            coinBasDroite=dimImage[0:2],
            profondeur=0,
            image=image,
        )
        # (TBR) Attention, les valeurs d'une image RVB doivent aller de 0 à 255, donc il vous faut régulariser votre image.
        valeurMaximaleRouge = np.max(image[:, :, 0])
        print(valeurMaximaleRouge)
        valeurMaximaleVert = np.max(image[:, :, 1])
        print(valeurMaximaleVert)
        valeurMaximaleBleu = np.max(image[:, :, 2])
        print(valeurMaximaleBleu)
        image[:, :, 0] /= valeurMaximaleRouge
        image[:, :, 1] /= valeurMaximaleVert
        image[:, :, 2] /= valeurMaximaleBleu
        image *= 255
        valeurMaximaleRouge = np.max(image[:, :, 0])
        print(valeurMaximaleRouge)
        valeurMaximaleVert = np.max(image[:, :, 1])
        print(valeurMaximaleVert)
        valeurMaximaleBleu = np.max(image[:, :, 2])
        print(valeurMaximaleBleu)
        return image.astype(
            int
        )  # On convertit le tableau de flottants en tableau d'entiers

    def lectureImage(self, image):
        """
        Met à jour l'arbre à partir de l'image. Modifie l'arbre en place.

        Parameters
        ----------
        image : numpy array
            Image à partir de laquelle créer un arbre.
        """

        dimImage = image.shape
        GrilleUtils.modifierRacine(
            racine=self.racine,
            numRacine=0,
            coinHautGauche=(0, 0),
            coinBasDroite=dimImage[0:2],
            image=image,
        )
        return None


# T = [i for i in range(1, 101)]
# Text = [20] * 100
# Tint = np.log(T)
# Pint = [100 * i for i in range(100)]
#
# a = Grille(1500, T, Text, Tint, Pint)
# a.racine = Feuille(a)
# # a.racine.ajoutFils(Feuille(a),forme='parallele')
