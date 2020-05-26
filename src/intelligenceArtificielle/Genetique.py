"""Implémentation de l'algorithme génétique."""
from operator import itemgetter  # Pour trier des listes
import random  # Pour introduire du hasard

from intelligenceArtificielle.structureDonnees.Arbre import (
    Arbre,
    Noeud,
    Feuille,
    Parallele,
    Serie,
)
from intelligenceArtificielle.GenerateurArbres import (
    GenerateurArbres,
)  # Utilisé en interne pour créer une population d'arbres aléatoires.
from intelligenceArtificielle.Autoencodeur import (
    Autoencodeur,
)  # L'interface permettant de manipuler les autoencodeurs
from intelligenceArtificielle.AutoencodeurDeterministe import (
    AutoencodeurDeterministe,
)  # Pour pouvoir instancier des autoencodeurs déterministes à partir de leurs noms.


class Genetique(object):
    """Classe pour l'algorithme génétique.

    Variables globales
    ------------------
    PROFONDEUR_MAX_ARBRE : int
    LARGEUR_MAX_ARBRE : int
    CHANCE_DE_MUTATION : float
    POURCENTAGE_CONSERVATION_FORT : float
        Pourcentage de la population qui va être gardé la génération suivante,
        sélectionne les meilleurs individus.
    CHANCE_SURVIE_FAIBLE : float
        Pourcentage de la population qui va être gardé la génération suivante,
        bien que ne figurant pas parmi les meilleurs individus.
    BIAIS_ALTERNANCE : float
        Le biais d'alternance est un biais qui pousse l'algorithme de création
        à créer des arbres avec une alternance de Serie/Parallele pour avoir des
        solutions plus intéressantes. Il doit être entre 0 (pas de biais
        d'alternance) et 0.5 (alternance forcée).
    ELAGUAGE_FORCE : bool
        Si ELAGUAGE_FORCE vaut True, alors chaque individu créé sera élagué pour
        tenir dans les dimension d'image spécifiées en argument du constructeur.
    SILENCE : bool
        Permet de lancer l'algorithme sans afficher d'information de debug dans
        la console.

    Attributs
    ---------
    population : list
        Liste des individus de la population. Chaque élément est un individu de
        type `Arbre`.
    Cint : float
        Capacité thermique associée à l'air intérieur.
    T : list
        La liste des temps (pour `Text`, `Tint`, `Pint`).
    Text : list
        La série des températures extérieures.
    Tint : list
        La série des températures intérieures.
    Pint : list
        La série des puissances intérieures.
    objectif : int
        L'objectif est le score de la fitness function à partir duquel on cesse
        de faire évoluer la population.
    taillePopulation : int
        La taille de la population à créer et à faire évoluer.
    generationMax : int
        Le nombre maximal d'itérations de l'algorithme.
    imageLargeur : int
        Dimensions des images.
    imageHauteur : int
        Dimensions des images.
    autoencodeur : AutoencodeurDeterministe
        Autoencodeur déterministe utilisé pour l'amélioration des arbres.
    """

    # Variables globales
    CHANCE_DE_MUTATION = 0.1
    POURCENTAGE_CONSERVATION_FORT = 0.5
    CHANCE_SURVIE_FAIBLE = 0.05
    ELAGUAGE_FORCE = True
    SILENCE = False

    def __init__(
        self,
        Cint,
        T,
        Text,
        Tint,
        Pint,
        taillePopulation=100,
        generationMax=1000,
        objectif=10,
        imageLargeur=32,
        imageHauteur=32,
        autoencodeur=None,
        modeGraphique=False,
    ):
        """Initialisation de la classe."""
        super(Genetique, self).__init__()
        self.Cint = Cint
        self.T = T
        self.Text = Text
        self.Tint = Tint
        self.Pint = Pint
        self.objectif = objectif
        self.taillePopulation = taillePopulation
        self.generationMax = generationMax
        self.imageLargeur = imageLargeur
        self.imageHauteur = imageHauteur
        # Si autoencodeur est None pendant l'algorithme génétique, alors la
        # phase d'amélioration des coefficients sera ignorée.
        if autoencodeur is None:
            self.autoencodeur = None
        elif type(autoencodeur) is str:
            # On peut aussi donner le nom d'un autoencodeur pour qu'il soit
            # récupéré depuis un fichier
            self.autoencodeur = AutoencodeurDeterministe(
                nomDuModele=autoencodeur,
                largeur=imageLargeur,
                hauteur=imageHauteur,
            )
        else:
            # On récupère l'autoencodeur directement de l'instance qui a été
            # fournie
            self.autoencodeur = autoencodeur
        # GénérateurArbres va automatiquement générer une population convenable
        # lors de sa construction sauf en mode graphique.
        self.generateur = GenerateurArbres(
            self.Cint,
            self.T,
            self.Text,
            self.Tint,
            self.Pint,
            self.taillePopulation,
            self.imageLargeur,
            self.imageHauteur,
            Genetique.ELAGUAGE_FORCE,
            modeGraphique,
        )
        # En mode graphique la population est initialisée plus tard avec la fonction génératrice de self.generateur (nommée populationAleatoireAnimee). Hors mode graphique, on récupère la population déjà initialisée.
        self.population = self.generateur.population

    def scorePopulation(self):
        """Calcule le score de la population.

        Renvoie une liste de couples (individu, score) triée par score sur toute
        la population. Les individus avec le meilleur score sont à la fin.
        """
        scoreIndividus = []
        if not Genetique.SILENCE:
            compteur = 0
            # Pour ne pas afficher le même message en boucle
            proportionsAffiche = []

        for individu in self.population:
            if not Genetique.SILENCE:
                proportion = 100 * compteur // self.taillePopulation
                if proportion % 5 == 0 and not proportion in proportionsAffiche:
                    proportionsAffiche.append(proportion)
                    print(f"{proportion}% de la population évalué.")
                compteur += 1
            scoreIndividus.append((individu, individu.score()))

        # On trie la liste selon l'argument d'indice 1, d'où le itemgetter.
        return sorted(scoreIndividus, key=itemgetter(1))

    def selection(self):
        """Ne conserve que les meilleurs individus de la population.

        Notes
        -----
        faiblesSurvivants
            Afin d'éviter de tomber dans des minimas locaux trop rapidement, on
            va faire survivre quelques individus faibles. On crée une liste
            dédiée pour que le dernier élément de la liste renvoyée à la fin de
            cette fonction soit bien le meilleur individu de la génération (ce
            qui n'est pas le cas si on fait directement un parent.append).
        """
        scoreIndividus = self.scorePopulation()

        # Le rang au delà duquel un individu dans la population est forcément
        # conservé.
        seuilSurvie = self.taillePopulation - int(
            Genetique.POURCENTAGE_CONSERVATION_FORT * self.taillePopulation
        )
        # On sélectionne les meilleurs individus dans la population.
        parents = scoreIndividus[seuilSurvie:]

        # cf. docstring pour `faiblesSurvivants`.
        faiblesSurvivants = []
        for individu in scoreIndividus[:seuilSurvie]:
            if random.random() < Genetique.CHANCE_SURVIE_FAIBLE:
                faiblesSurvivants.append(individu)

        parents = faiblesSurvivants + parents
        return [list(i) for i in zip(*parents)]

    def mutation(self):
        """Affecte des mutations à certains individus de la population.

        Pour l'instant, on utilise un taux de mutation constant.
        """
        for individu in self.population:
            # On note si l'individu a été muté, auquel cas il faudra l'élaguer
            # si cela est demandé pour qu'il reste représentable sous forme
            # d'image.
            besoinElaguage = False
            # On peut muter un même individu plusieurs fois si le hasard le veut
            while random.random() < Genetique.CHANCE_DE_MUTATION:
                besoinElaguage = True
                profondeur = len(individu.forme)
                # On tire une profondeur à laquelle faire la mutation.
                choixProfondeur = random.randrange(profondeur)
                # Le nombre de noeuds à la profondeur donnée.
                largeur = individu.forme[choixProfondeur]
                # On choisit un individu au hasard parmi ceux à cette profondeur.
                choixLargeur = random.randrange(largeur)
                # On récupère l'individu tiré au hasard.
                noeud = individu.inspecter(choixProfondeur, choixLargeur)

                # On tire aléatoirement entre True et False avec équiprobabilité.
                action = random.random() > 0.5

                # L'action sera différente si le noeud tiré est une `Feuille` ou
                # non.
                if type(noeud) is Feuille:
                    # On va ajouter une feuille à ce noeud.
                    fils = Feuille()
                    if action:
                        # 50% de chances d'ajouter en série
                        noeud.ajoutFils(fils, forme="serie")
                    else:
                        # 50% de chances d'ajouter en parallèle
                        noeud.ajoutFils(fils, forme="parallele")
                else:
                    nombreFils = len(noeud.fils)

                    if action:
                        # 50% de chances d'ajouter un enfant.
                        # On tire un indice sur le lequel faire notre action
                        # dans 0, `nombreFils` inclu.
                        choixIndex = random.randrange(nombreFils + 1)
                        fils = Feuille()
                        noeud.ajoutFils(fils, index=choixIndex)
                    else:
                        # 50% de chances de supprimer un fils.
                        # On tire un indice sur le lequel faire notre action
                        # dans 0, `nombreFils` exclu.
                        choixIndex = random.randrange(nombreFils)
                        noeud.suppressionFils(index=choixIndex)

            if besoinElaguage:
                # On remet l'indicateur à 0 pour le prochain individu.
                besoinElaguage = False
                if Genetique.ELAGUAGE_FORCE:
                    # Si besoin, on élague l'individu obtenu
                    individu.elaguer(
                        largeur=self.imageLargeur, hauteur=self.imageHauteur
                    )

    def fusion(self):
        """Fusionne les individus.

        On ajoutera tous les enfants d'un seul coup à la fin pour éviter de
        faire une fusion sur un enfant qui vient d'être créé.
        """
        enfants = []
        # On calcule le nombre d'individus qu'il nous reste à produire pour
        # compléter la génération suivante.
        populationManquante = self.taillePopulation - len(self.population)

        for i in range(populationManquante):
            # On tire deux individus dans la population sans faire de remise.
            pere, mere = random.sample(self.population, k=2)

            # Il nous faut à présent déterminer la profondeur maximale jusqu'à
            # laquelle les deux parents ont une forme commune.
            profondeurSemblable = 0
            # On teste toutes les profondeurs et on s'arrète à la première non
            # commune.
            for j in range(min(len(pere.forme), len(mere.forme))):
                # print(f"{j} {pere.forme[j]} {mere.forme[j]}")
                if pere.forme[j] != mere.forme[j]:
                    if j == 0:
                        print(pere.forme)
                        print(mere.forme)
                    profondeurSemblable = j - 1
                    break

            # Le sommet qui va nous servir à créer le nouvel enfant
            sommet = None
            # On tire au hasard le parent dont on va récupérer le sommet.
            choixSommet = random.random() > 0.5
            if choixSommet:
                sommet = mere.racine.sousArbre()
            else:
                sommet = pere.racine.sousArbre()

            # On crée l'objet `Arbre` qui acueille le sommet. Le constructeur
            # de `Arbre` dispose d'une syntaxe spéciale concue pour attacher
            # une racine direcetement.
            enfant = Arbre(
                self.Cint,
                self.T,
                self.Text,
                self.Tint,
                self.Pint,
                racine=sommet,
            )

            # Le nombre de noeuds qui vont devoir être fusionnés entre parent et
            # enfant.
            largeur = enfant.forme[profondeurSemblable]
            # On réalise l'étape de fusion pour tous les noeuds de
            # `profondeurSemblable`.
            for j in range(largeur):
                # On récupère le noeud correspondant pour la mere, le pere et
                # l'enfant.
                noeudPere = pere.inspecter(profondeurSemblable, j)
                noeudMere = mere.inspecter(profondeurSemblable, j)
                noeudEnfant = enfant.inspecter(profondeurSemblable, j)
                # On crée la liste de tous les nouveaux enfants possibles.
                # Un détail d'implémentation : en théorie on devrait faire un
                # choix parmi les `sousArbre` crées à partir des enfants de pere
                # et mere, mais créer un `sousArbre` peut être un peu long, donc
                # en créer qui ne seront pas utilisés est une perte de temps.
                # Au lieu de cela, on va faire notre choix sur les enfants
                # directs de pere et mere, puis calculer le `sousArbre` des
                # enfants élus, ce qui est plus efficace mais amène au même
                # résultat.
                if type(noeudEnfant) is Feuille:
                    # Si on tombe sur une feuille, on ne peut évidemment pas y
                    # ajouter de fils.
                    continue
                filsPotentiels = noeudPere.fils + noeudMere.fils
                # On détermine le nombre d'enfants à donner à l'enfant.
                nombreFils = len(filsPotentiels) // 2 + 1
                # On choisit nombreFils éléments parmi filsPotentiels sans
                # remise.
                filsChoisis = random.sample(filsPotentiels, k=nombreFils)
                # On calcule le sousArbre des enfants choisis avant de l'ajouter
                # à l'enfant.
                sousArbresChoisis = [fils.sousArbre() for fils in filsChoisis]
                # Enfin, on ajoute les nouveaux sous arbres créés sous le noeud
                # choisi de enfant.
                noeudEnfant.substituerEnfants(sousArbresChoisis)

            if Genetique.ELAGUAGE_FORCE:
                # Si besoin, on élague l'enfant obtenu pour qu'il soit
                # représentable sous forme d'image.
                enfant.elaguer(
                    largeur=self.imageLargeur, hauteur=self.imageHauteur
                )

            # On ajoute l'arbre créé à la population de descendants.
            enfants.append(enfant)
        # On renvoie la liste des enfants créés pour qu'ils soient ajoutés à la
        # population.
        return enfants

    def ameliorerPopulation(self):
        """Effectue une génération de l'algorithme génétique.

        Renvoie quelques valeurs qui sont utiles pour l'affichage."""

        # SELECTION
        if not Genetique.SILENCE:
            print("Selection")
        self.population, scores = self.selection()

        # On crée une copie du meilleur individu de la génération
        # (il risque d'être modifié par mutation).
        meilleurArbre = self.population[-1].racine.sousArbre()
        meilleurIndividu = Arbre(
            self.Cint,
            self.T,
            self.Text,
            self.Tint,
            self.Pint,
            racine=meilleurArbre,
        )

        # AMELIORATION
        if self.autoencodeur is not None:
            if not Genetique.SILENCE:
                print("Amelioration")
            self.autoencodeur.ameliorerArbres(self.population)

        # MUTATION
        if not Genetique.SILENCE:
            print("Mutation")
        self.mutation()

        # FUSION
        if not Genetique.SILENCE:
            print("Fusion")
        self.population += self.fusion()

        # On renvoie des valeurs qui pourront être utiles pour l'affichage
        # (le meilleur individu et son score).
        return meilleurIndividu, scores[-1]

    def optimisation(self):
        """Réalise l'optimisation de la population par l'algorithme génétique.

        Il s'agit d'une fonction génératrice qui "yield" les valeurs
        intéressantes pour l'animation de l'interface graphique à chaque
        génération. Une fois l'algorithme terminé, le résultat de l'algorithme
        est contenu dans les différents attributs de l'objet.
        """
        # Pour que le premier generation renvoyé soit bien 0
        generation = -1
        meilleurScore = 2 * self.objectif
        while (generation < self.generationMax) and (
            abs(meilleurScore) > self.objectif
        ):
            meilleurIndividu, meilleurScore = self.ameliorerPopulation()
            generation += 1
            yield generation, meilleurIndividu, meilleurScore
