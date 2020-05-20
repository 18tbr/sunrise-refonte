from operator import itemgetter  # Permettre de trier des listes
import random  # Permettre d'introduire du hasard

from Grille import Grille, Noeud, Feuille, Parallele, Serie


class Genetique(object):
    """docstring for Genetique."""

    # Valeurs globales de la classe génétique
    PROFONDEUR_MAX_ARBRE = 100
    LARGEUR_MAX_ARBRE = 50
    CHANCE_DE_MUTATION = 0.1
    POURCENTAGE_CONSERVATION_FORT = 0.5  # Pourcentage de la population qui va être gardé la génération suivante, les meilleurs individus
    CHANCE_SURVIE_FAIBLE = 0.05  # Pourcentage de la population qui va être gardé la génération suivante, bien que ne figurant pas parmis les meilleurs individus

    # def __init__(self, Cint, T, Text, Tint, Pint, taillePopulation=100, generationMax=1000, objectif = 10, numeroGeneration):
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
    ):
        super(Genetique, self).__init__()
        # Liste des individus de la population - chaque individu de type Grille
        self.population = []
        # Capacité thermique associée à l'air intérieur
        self.Cint = Cint
        # La liste des temps (pour Text, Tint, Pint)
        self.T = T
        # La série des températures extérieures
        self.Text = Text
        # La série des températures intérieures
        self.Tint = Tint
        # La série des puissances intérieures
        self.Pint = Pint
        # L'objectif est le score de la fitness function à partir duquel on cesse de faire évoluer la population
        self.objectif = objectif

        self.taillePopulation = taillePopulation
        self.generationMax = generationMax

        # On initialise directement la population à partir du constructeur
        self.populationAleatoire()
        # self.numeroGeneration = numeroGeneration

    def scorePopulation(self):
        # Calcule le score de la population, renvoie une liste de doublet (individu, score) triée par score sur toute la population. Les individus avec le meilleur score sont au début.
        scoreIndividus = []
        compteur = 0
        proportionsAffiche = (
            []
        )  # Pour ne pas afficher le même message en boucle
        for individu in self.population:
            proportion = 100 * compteur // self.taillePopulation
            if proportion % 5 == 0 and not proportion in proportionsAffiche:
                proportionsAffiche.append(proportion)
                print(f"{proportion}% de la population évalué.")
            compteur += 1
            scoreIndividus.append((individu, individu.score()))
        # On trie la liste selon l'argument d'indice 1, d'où le itemgetter
        return sorted(scoreIndividus, key=itemgetter(1))

    def populationAleatoire(self):
        # On remet la population à zéro au cas où.
        self.population = []
        proportionsAffiche = []
        # Méthode qui sert à générer un population aléatoire facilement
        for i in range(self.taillePopulation):
            # Dans la mesure où la génération de population est assez longue, on se permet d'afficher des messages pour maintenir l'utilisateur éveillé.
            proportion = 100 * i // self.taillePopulation
            if proportion % 5 == 0 and proportion not in proportionsAffiche:
                proportionsAffiche.append(proportion)
                print(f"{proportion}% de la population créé.")
            self.population.append(self.individuAleatoire())

    def individuAleatoire(self):
        # On initialise l'individu que l'on va créer
        individu = Grille(self.Cint, self.T, self.Text, self.Tint, self.Pint)

        # On tire aléatoirement la profondeur qu'aura notre individu
        profondeur = random.randint(1, Genetique.PROFONDEUR_MAX_ARBRE)

        # On crée itérativement tous les niveaux de notre arbre
        for i in range(profondeur - 1):
            # Pour éviter des configurations absurdes on force l'arbre à avoir une forme un peu conique (c'est à dire à n'avoir pas trop de fils sur les premières générations).
            largeurAutorisee = min(Genetique.LARGEUR_MAX_ARBRE, 3 * profondeur)
            # On détermine au hasard la largeur de la profondeur i+1
            largeur = random.randint(1, largeurAutorisee)

            # On choisit (avec remise) les noeuds de la génération i qui accueilleront des enfants à la génération i+1
            indicesChoisis = random.choices(
                population=range(individu.forme[i]), k=largeur
            )

            # On ajoute les enfants aux parents désignés
            for k in indicesChoisis:
                # Le noeud auquel on doit ajouter un enfant. Un même indice peut être tiré plusieurs fois.
                parent = individu.inspecter(i, k)
                enfant = Feuille()
                if type(parent) is Feuille:
                    # Hasard a 50% d'être vrai (et 50% d'être faux) et nous permet de choisir entre ajouter un fils en série et en parallèle
                    hasard = random.random() > 0.5
                    if hasard:
                        parent.ajoutFils(enfant, forme="serie")
                    else:
                        parent.ajoutFils(enfant, forme="parallele")
                else:
                    # On tire aléatoirement l'index où l'on va insérer le nouvel enfant parmi les enfants préexistants du parent. Le +1 correspond au fait que l'on peut insérer un enfant tout à la fin de la liste des descendants du parent.
                    indexAleatoire = random.randrange(len(parent.fils) + 1)
                    # On insère le nouvel enfant
                    parent.ajoutFils(enfant, index=indexAleatoire)

        # On renvoie la liste ainsi formée
        return individu

    def selectionPopulation():
        # Réduit la population pour n'en conserver que les meilleurs individus
        scoreIndividus = self.scorePopulation()
        individus = [elt[0] for elt in scoreIndividus]

        # Le rang au dela duquel un individu dans la population est forcémentconservé
        seuilSurvie = self.taillePopulation - int(
            Genetique.POURCENTAGE_CONSERVATION_FORT * self.taillePopulation
        )
        # On sélectionne les meilleurs individus dans la population
        parents = individus[seuilSurvie:]

        # Afin d'éviter de tomber dans des minimas locaux trop rapidement, on va faire survivre quelques individus faibles
        for individu in individus[:seuilSurvie]:
            if randoms.random() < Genetique.CHANCE_SURVIE_FAIBLE:
                parents.append(individu)

        return parents

    # Fonction qui va faire évoluer la population d'une génération à une autre
    # Sélection
    # Mutation
    # Fusion
    # Renvoie la population de la prochaine génération ainsi que la distribution triée des différents scores des arbres de la population et les différentes températures au cours du temps Tint pour le meilleur arbre
    def ameliorerPopulation(self):

        # SELECTION
        self.selectionPopulation()

        # MUTATION

        # Il s'agirait ici de faire la mutation
        for individu in parents:
            if random() < Genetique.CHANCE_DE_MUTATION:
                # individu va être modifié
                forme = individu.forme

                nombreModifications = random.randint(1, len(forme))
                for i in range(nombreModifications):
                    profondeur = random.randint(0, len(forme) - 1)
                    indice = random.randint(0, forme[profondeur] - 1)
                    noeudChoisi = individu.inspecter(profondeur, indice)
                    # Vision du monde manichéenne, soit optique de rajouter du nouveau (1), soit de supprimer (0)

                    action = random.randint(0, 1)

                    if type(noeudChoisi) == Feuille:
                        if action == 1:
                            format = random.randint(1, 2)
                            if format == 1:
                                noeudChoisi.ajoutFils(
                                    Feuille(individu), forme="serie"
                                )
                            if format == 2:
                                noeudChoisi.ajoutFils(
                                    Feuille(individu), forme="parallele"
                                )
                    else:
                        if action == 0:
                            nombreFils = len(noeudChoisi.fils)
                            indiceFilsEnlevé = random.randint(0, nombreFils - 1)
                            noeudChoisi.fils.remove(indiceFilsEnlevé)
                        else:
                            taille = len(noeudChoisi.fils)
                            indice_ajout = random.randint(0, taille)
                            noeudChoisi.ajoutFils(
                                Feuille(individu), indice_ajout
                            )

        # CROSSOVER
        nombreParents = len(parents)
        populationManquante = self.taillePopulation - nombreParents
        enfants = []

        while len(enfants) < populationManquante:
            # On choisit on hasard le père et la mère
            indexPere = random.randint(0, self.taillePopulation - 1)
            indexMere = indexPere
            while indexMere == indexPere:
                indexMere = random.randint(0, self.taillePopulation - 1)
            pere = self.population[indexPere]
            mere = self.population[indexPere]

            # On détermine la profondeur maximale où les deux parents ont le même format
            i = 0
            while (
                (i < len(pere.forme))
                & (i < len(mere.forme))
                & (pere.forme[i] == mere.forme[i])
            ):
                i = i + 1
            i = i - 1
            enfant = Grille(self.cint, self.T, self.Text, self.Tint, self.Pint)
            enfant.racine = pere.sousArbre()

            for j in range(pere.forme[i]):
                petitPere = pere.inspecter(i, j)
                petiteMere = mere.inspecter(i, j)
                filsPotentiels = petitPere.fils + petiteMere.fils
                nombreFils = (len(petitPere.fils) + len(petiteMere.fils)) // 2
                filsChoisis = random.choices(filsPotentiels, k=nombreFils)
                enfant.substituerEnfants(filsChoisis)

            # La population de la génération suivante
            return (
                (parents + enfants),
                [scoreIndividus[k][1] for k in range(0, len(scoreIndividus))],
                [vecteur[0] for vecteur in scoreIndividus[0][0].Simulation().y],
            )

    def AlgoGenetique(self):
        Generation = Genetique(
            cint=self.cint,
            T=self.T,
            Text=self.Text,
            Tint=self.Tint,
            Pint=self.Pint,
            objectif=self.objectif,
            numeroGeneration=1,
        )
        i = 1
        meilleurScore = 2 * self.objectif
        while (i < self.generationMax) & abs(meilleurScore) > self.objectif:
            [
                Generation,
                DistributionScore,
                TemperatureMeilleurArbre,
            ] = Generation.ameliorerPopulation()
            Generation.numeroGeneration += 1
            meilleurScore = abs(DistributionScore[0])
            i += 1
        return Generation[0], DistributionScore[0], TemperatureMeilleurArbre[0]
