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
    logit,
)  # Une implémentation de la fonction sigmoïde utilisée pour normaliser les valeurs des coefficients pour les mettre dans les images. Logit est la fonction inverse de expit.

# Notez que pour importer ces classes dans les autres modules, il est préférable de faire "from Arbre import Noeud, ..." plutôt que d'importer directement les fichiers concernés.
from intelligenceArtificielle.structureDonnees.Noeud import Noeud
from intelligenceArtificielle.structureDonnees.Feuille import Feuille
from intelligenceArtificielle.structureDonnees.SunRiseException import (
    FeuilleException,
    NonFeuilleException,
    NonMarqueException,
    SimulationException,
)
from intelligenceArtificielle.structureDonnees.Serie import Serie
from intelligenceArtificielle.structureDonnees.Parallele import Parallele
import intelligenceArtificielle.structureDonnees.Coefficients as Coefficients

from math import ceil


class Arbre(object):
    """docstring for Arbre."""

    # Quelque valeurs statiques d'ordre de grandeur de capacité thermique, coefficient de transmission thermique et (pour avoir une symétrie dans le code) une valeur de référence pour l'erreur propagée qui doit rester à 100. Le fait de partager ces valeurs pour tous les obets de la classe Arbre permet de comparer plusieurs images obtenues simplement et de simplifier le travail de l'autoencodeur.
    referenceConductance = Coefficients.referenceH
    referenceCapacite = Coefficients.referenceC
    referenceErreur = Coefficients.referenceE

    def __init__(self, cint, T, Text, Tint, Pint, racine=None):
        super(Arbre, self).__init__()
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
        # IMPORTANT : ne pas ajouter une feuille avant d'avoir défini la forme de l'arbre
        # La racine de l'arbre. Cet argument optionnel a été ajouté pour simplifier la syntaxe de la fonction fusion.
        if racine is None:
            self.racine = Feuille(self)
        else:
            self.racine = racine
            self.racine.attacher(self)

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

        def diff(t, T):
            # dT/dt = diff(T,t) = C * (AT + BQ)
            # Notez que self.Text et self.Pint sont des interpolations par spline des Text et Pint passés en argument à l'origine.
            return C @ (A @ T + B @ np.array([[self.Text(t)], [self.Pint(t)]]))

        # Attention à la façon dont solve_ivp fonctionne et en particulier à t_span et t_eval (qui sont différents d'odeint si ma mémoire est bonne).
        return solve_ivp(
            fun=diff,
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

        def diff(t, T):
            # dT/dt = diff(T,t) = C * (AT + BQ)
            # Notez que self.Text et self.Pint sont des interpolations par spline des Text et Pint passés en argument à l'origine.
            return C @ (A @ T + B @ np.array([[self.Text(t)], [self.Pint(t)]]))

        # Attention à la façon dont solve_ivp fonctionne et en particulier à t_span et t_eval (qui sont différents d'odeint si ma mémoire est bonne).
        calcul = solve_ivp(
            fun=diff,
            t_span=(self.T[0], self.T[-1]),
            y0=T0,
            method="RK45",
            t_eval=self.T,
            vectorized=True,
        )

        if not calcul.success:
            raise SimulationException(
                "La simulation de l'arbre n'a pas pu être menée à son terme."
            )

        calculTint = calcul.y[0]
        ecart = self.Tint - calculTint
        # On calcule maintenant l'intégrale de l'erreur pour Tint sur toute la simulation
        epsilon = np.sum(ecart, 0)

        # Fonction de pénalité de proximité temporelle
        pi = lambda t: 1 / (1 + t / delay)

        # On alloue le vecteur des erreurs propagées.
        E = [0 for i in range(nbTemperatures)]

        # On initialise en notant l'erreur associée à Tint que l'on va essayer de propager.
        try:
            E[0] = epsilon
        except OverflowError:
            raise SimulationException(
                "L'erreur obtenue sur cette arbre est trop grande pour permettre un traitement numérique correct."
            )
        # La file qui nous permet de traiter de façon cohérente toutes le températures
        fileTraitementTemperature = [0]
        for i in range(nbTemperatures):
            if min(E) > 0:
                # Si jamais on a alloué une erreur à toutes les températures internes, on peut arrêter notre boucle en avance.
                break
            else:
                if i == len(fileTraitementTemperature):
                    # Si la file est vide par construction on a fini notre travail
                    break
                # On traite la première température possible
                t = fileTraitementTemperature[i]
                for j in range(nbTemperatures):
                    if E[j] == 0:  # Sinon la température a déjà été atteinte
                        delayIJ = D[i, j]
                        if delayIJ != 0:
                            # Formule de rétropropagation heuristique de l'erreur
                            try:
                                E[j] = E[i] * pi(delayIJ)
                            except ValueError:
                                raise SimulationException(
                                    "L'erreur obtenue sur cette arbre est trop grande pour permettre un traitement numérique correct."
                                )
                            fileTraitementTemperature.append(j)

        return E

    def score(self):
        # On calcule toutes le températures internes au fil du temps
        calcul = self.simulation()
        if not calcul.success:
            raise SimulationException(
                "La simulation de l'arbre n'a pas pu être menée à son terme."
            )
        # On récupère la température intérieure (la première dans la matrice). Attention, la façon dont solve_ivp restitue les températures n'est pas la même que pour odeint.
        calculTint = calcul.y[0]
        # On calcule l'écart entre la température calculée et la référence
        ecart = self.Tint - calculTint
        # On renvoie l'opposé de l'écart quadratique cumulé. Comme cela plus le score est grand, plus l'arbre est bon, ce qui est plus intuitif pour l'algorithme génétique.
        # score = -np.sum(np.square(ecart), 0)
        # Le calcul précédent a de forts problèmes d'overflow en pratique, donc on en propose une formulation alternative qui devrait poser moins de problèmes. On propose d'utiliser la moyenne à la place, qui sera plus petite mais différente seulement d'un coefficient multiplicatif qui est constant sur tous les arbres.
        score = -np.mean(np.square(ecart), 0)
        if score == float("Nan") or score == -float("Inf"):
            raise SimulationException(
                "L'erreur obtenue sur cette arbre est trop grande pour permettre un traitement numérique correct."
            )
        # else ...
        return score

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

    def ecritureImage(self, largeur=32, hauteur=32):
        """
        Convertit un arbre en image.

        Parameters
        ----------
        largeur est la largeur horizontale de l'image en nombre de cases
        hauteur est la hauteur verticale de l'image en nombre de cases
        """
        # Avant de pouvoir écrire l'image il faut marquer les feuilles de l'arbre
        self.marquage()

        # Le 3 correspond aux trois couleurs de notre image
        image = np.zeros((hauteur, largeur, 3))

        # On colore récursivement l'image depuis la racine
        self.racine.dessiner(
            image, coinHautGauche=(0, 0), coinBasDroite=(hauteur, largeur)
        )

        # La plupart des autoencodeurs préfèrent travailler avec des coefficients dans 0,1 plutôt que dans 0, 255 donc on n'a pas besoin de passer nos valeurs sous forme d'entiers.
        sigRouge = np.vectorize(
            lambda t: expit(t / Arbre.referenceConductance), otypes=[float],
        )
        sigVert = np.vectorize(
            lambda t: expit(t / Arbre.referenceCapacite), otypes=[float],
        )
        sigBleu = np.vectorize(
            lambda t: expit(t / Arbre.referenceErreur), otypes=[float],
        )

        # print("Ecriture rouge:", np.mean(image[:, :, 0]))
        # print("Ecriture vert:", np.mean(image[:, :, 1]))

        image[:, :, 0] = sigRouge(image[:, :, 0])
        image[:, :, 1] = sigVert(image[:, :, 1])
        image[:, :, 2] = sigBleu(image[:, :, 2])

        return image

    def lectureImage(self, image):
        """
        Met à jour l'arbre à partir de l'image. Modifie l'arbre en place.

        Parameters
        ----------
        image : numpy array
            Image à partir de laquelle créer un arbre. Attention, cette image sera détruite pendant la lecture.
        """
        hauteur, largeur, couleurs = image.shape
        # Avant de donner l'image pour mettre à jour notre arbre, il faut repasser les valeurs (qui sont sur [0,1]) en valeurs réelles.
        invSigRouge = np.vectorize(
            lambda t: logit(t) * Arbre.referenceConductance, otypes=[float],
        )
        invSigVert = np.vectorize(
            lambda t: logit(t) * Arbre.referenceCapacite, otypes=[float]
        )
        invSigBleu = np.vectorize(
            lambda t: logit(t) * Arbre.referenceErreur, otypes=[float]
        )

        image[:, :, 0] = invSigRouge(image[:, :, 0])
        image[:, :, 1] = invSigVert(image[:, :, 1])
        image[:, :, 2] = invSigBleu(image[:, :, 2])

        # print("Lecture rouge:", np.mean(image[:, :, 0]))
        # print("Lecture vert:", np.mean(image[:, :, 1]))

        propositionCint = self.racine.lire(
            image,
            coinHautGauche=(0, 0),
            coinBasDroite=(hauteur, largeur),
            conteneur=None,
        )

        # Cette valeur n'est pas utilisée par la suite, mais dans la mesure où elle est calculée on peut toujours l'afficher.
        # print("propositionCint:", propositionCint)

    def normalisationImage(self, image):
        # Sert à normaliser une image sans modifier l'arbre, utile en particulier pour l'entrainement des autoencodeurs
        hauteur, largeur, couleurs = image.shape
        self.racine.normaliser(
            image, coinHautGauche=(0, 0), coinBasDroite=(hauteur, largeur)
        )
        # Pour plus de facilité, on renvoie l'image (qui est modifiée par effet de bord)
        return image

    def elaguer(self, largeur, hauteur):
        # Cette fonction sert à modifier un arbre de sorte à le forcer à tenir dans le format d'image demandé. Les enfants qui ne tiennent pas dans l'image seront supprimés de l'arbre
        self.racine.elaguerSousArbre(
            coinHautGauche=(0, 0), coinBasDroite=(hauteur, largeur)
        )
