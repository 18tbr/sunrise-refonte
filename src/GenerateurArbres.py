# Ce fichier contient une classe permettant d'initialiser une population d'arbres aléatoire. Cette fonctionnalité a été séparée de la classe Génétique pour éviter des problèmes de dépendances circulaires

import random

from Grille import Grille, Feuille, Serie, Parallele, Noeud

class GenerateurArbres(object):
    """docstring for GenerateurArbres."""

    PROFONDEUR_MAX_ARBRE = 100
    LARGEUR_MAX_ARBRE = 50
    BIAIS_ALTERNANCE = 0.2

    def __init__(
        self,
        Cint,
        T,
        Text,
        Tint,
        Pint,
        taillePopulation=100,
        imageLargeur=32,
        imageHauteur=32,
        elaguageForce=True
    ):
        """Initialisation de la classe."""
        super(GenerateurArbres, self).__init__()
        self.population = []
        self.Cint = Cint
        self.T = T
        self.Text = Text
        self.Tint = Tint
        self.Pint = Pint
        self.taillePopulation = taillePopulation
        self.imageLargeur = imageLargeur
        self.imageHauteur = imageHauteur
        # Notez que contrairement à Genetique, l'élaguage forcé est ici un paramètre, ce qui évite d'avoir deux valeurs incohérentes dans les deux classes.
        self.elaguageForce = elaguageForce
        # On initialise directement la population à partir du constructeur.
        self.populationAleatoire()

    def populationAleatoire(self):
        """Génère une population aléatoire."""
        # On remet la population à zéro au cas où.
        self.population = []
        proportionsAffiche = []

        for i in range(self.taillePopulation):
            # La génération de population est assez longue, on affiche des
            # messages pour maintenir l'utilisateur éveillé.
            proportion = 100 * i // self.taillePopulation
            if proportion % 5 == 0 and proportion not in proportionsAffiche:
                proportionsAffiche.append(proportion)
                print(f"{proportion}% de la population créé.")
            self.population.append(self.individuAleatoire())


    def individuAleatoire(self):
        """Génère un individu aléatoire.

        Notes
        -----
        graineAlternance : float
            `graineAlternance` est une graine qui détermine si l'alternance
            devrait commencer par des liaisons séries ou parallèles.
            `graineAlternance` peut prendre les valeurs
            -Genetique.BIAIS_ALTERNANCE ou Genetique.BIAIS_ALTERNANCE.
        hasard : bool
            `hasard` a 50% de chances d'être vrai et 50% d'être faux et nous
            permet de choisir entre ajouter un fils en série et en parallèle.
            `graineAlternance` permet de favoriser tantôt les liaisons séries,
            tantôt les liaisons parallèles.
        largeurAutorisee : int
            Pour éviter des configurations absurdes, on force l'arbre à avoir
            une forme un peu conique (c'est-à-dire à n'avoir pas trop de fils
            sur les premières générations).
        """
        graineAlternance = (
            GenerateurArbres.BIAIS_ALTERNANCE
            + 2 * (random.random() > 0.5) * GenerateurArbres.BIAIS_ALTERNANCE
        )

        # On initialise l'individu que l'on va créer.
        individu = Grille(self.Cint, self.T, self.Text, self.Tint, self.Pint)
        # On tire aléatoirement la profondeur qu'aura notre individu.
        profondeur = random.randint(1, GenerateurArbres.PROFONDEUR_MAX_ARBRE)

        # On crée itérativement tous les niveaux de notre arbre.
        for i in range(profondeur - 1):
            # cf. docstring pour `largeurAutorisee`.
            # Notez que la largeur réelle d'une couche de l'arbre dépasse
            # souvent la largeur maximale autorisée. En effet, lorsque l'on
            # ajoute un fils a une feuille, cette dernière descend dans la
            # nouvelle profondeur. On se retrouve donc avec deux noeuds de plus
            # à la nouvelle profondeur au lieu d'un.
            largeurAutorisee = min(GenerateurArbres.LARGEUR_MAX_ARBRE, 3 * (i+1))
            # On détermine au hasard la largeur de la profondeur i+1.
            largeur = random.randint(1, largeurAutorisee)

            # On choisit (avec remise) les noeuds de la génération i qui
            # accueilleront des enfants à la génération i+1.
            indicesChoisis = random.choices(
                population=range(individu.forme[i]), k=largeur
            )

            # On ajoute les enfants aux parents désignés.
            for k in indicesChoisis:
                # Le noeud auquel on doit ajouter un enfant. Un même indice peut
                # être tiré plusieurs fois.
                parent = individu.inspecter(i, k)
                enfant = Feuille()
                if type(parent) is Feuille:
                    # cf. docstring pour `hasard`.
                    hasard = random.random() > (0.5 + graineAlternance)
                    if hasard:
                        parent.ajoutFils(enfant, forme="serie")
                    else:
                        parent.ajoutFils(enfant, forme="parallele")
                else:
                    # On tire aléatoirement l'index où l'on va insérer le nouvel
                    # enfant parmi les enfants préexistants du parent. Le +1
                    # correspond au fait que l'on peut insérer un enfant tout à
                    # la fin de la liste des descendants du parent.
                    indexAleatoire = random.randrange(len(parent.fils) + 1)
                    # On insère le nouvel enfant.
                    parent.ajoutFils(enfant, index=indexAleatoire)
            # On alterne le biais entre liaisons séries et parallèle.
            graineAlternance *= -1

        # Si on a demandé un élaguage automatique, alors on tronque l'individu pour qu'il soit représentable sous forme d'image.
        if self.elaguageForce:
            individu.elaguer(largeur=self.imageLargeur, hauteur=self.imageHauteur)
        # On renvoie la liste ainsi formée.
        return individu
