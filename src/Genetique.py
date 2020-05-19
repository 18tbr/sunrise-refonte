from operator import itemgetter  # Permettre de trier des listes
import random  # Permettre d'introduire du hasard

from Grille import Grille, Noeud, Feuille, Parallele, Serie

class Genetique(object):
    """docstring for Genetique."""

    def __init__(self, cint, T, Text, Tint, Pint, objectif, numeroGeneration):
        super(Genetique, self).__init__()
        # Liste des individus de la population - chaque individu de type Grille
        self.population = []
        # Capacité thermique associée à l'air intérieur
        self.cint = cint
        # La liste des temps (pour Text, Tint, Pint)
        self.T = T
        # La série des températures extérieures
        self.Text = Text
        # La série des températures intérieures
        self.Tint = Tint
        # La série des puissances intérieures
        self.Pint = Pint
        #L'objectif est le score de la fitness function à partir duquel on cesse de faire évoluer la population
        self.objectif = objectif

        self.numeroGeneration = numeroGeneration

        self.PROFONDEUR_MAX_ARBRE = 100
        self.LARGEUR_MAX_ARBRE = 50

        self.CHANCE_DE_MUTATION = 0.1
        self.POURCENTAGE_CONSERVATION_FORT = 0.2  # Pourcentage de la population qui va être gardé la génération suivante, les meilleurs individus
        self.CHANCE_SURVIE_FAIBLE = 0.05  # Pourcentage de la population qui va être gardé la génération suivante, bien que ne figurant pas parmis les meilleurs individus
        self.TAILLE_POPULATION = 100
        self.GENERATION_MAX = 100000


    # NB: valeur sûrement à changer, arbitraire

    def scorePopulation(self):
        # Calcule le score de la population, renvoie une liste de doublet (individu, score) triée par score sur toute la population. Les individus avec le meilleur score sont au début.
        scoreIndividus = []
        for individu in self.population:
            scoreIndividus.append((individu, individu.score()))
        return sorted(scoreIndividus, key=itemgetter(1), reverse=True)

    def populationAleatoire(self):
        for i in range(self.TAILLE_POPULATION):
            self.population.append(self.individuAleatoire())

    def individuAleatoire(self):
        profondeur = random.randint(1, self.PROFONDEUR_MAX_ARBRE)
        individu = Grille(self.cint, self.T, self.Text, self.Tint, self.Pint)
        # Série (1) / Parallèle (2) / Rien (3)


        for i in range(profondeur-1):
            print(i)
            # On détermine au hasard la largeur de la généation suivante
            largeur = random.randint(1, self.LARGEUR_MAX_ARBRE)

            # On répartit les différents éléments sur les différents indices
            listeIndices = [k for k in range(0, largeur)]
            indicesChoisis = random.choices(
                listeIndices, k=max(0,(individu.forme[i] - 1))
            )
            indicesChoisis.append(0)
            indicesChoisis.append(individu.forme[i] - 1)
            indicesChoisis.sort()

            # on créé alors le nombre de fils correspondant
            for k in range(individu.forme[i]):
                parent = individu.inspecter(i, k)
                n_fils = indicesChoisis[k + 1] - indicesChoisis[k]
                if n_fils > 0:
                    hasard = random.randint(1, 2)
                    if hasard == 1:
                        parent = parent.ajoutFils(individu, forme="serie")

                        for j in range(n_fils):
                            parent.ajoutFils(individu, index=j)
                    else:
                        parent = parent.ajoutFils(individu, forme="parallele")

                        for j in range(n_fils):
                            parent.ajoutFils(individu, index=j)

    # Fonction qui va faire évoluer la population d'une génération à une autre
    # Sélection
    # Mutation
    # Fusion
    # Renvoie la population de la prochaine génération ainsi que la distribution triée des différents scores des arbres de la population et les différentes températures au cours du temps Tint pour le meilleur arbre
    def ameliorerPopulation(self):

        # SELECTION
        scoreIndividus = self.scorePopulation()

        # On a les meilleurs individus qu'on sélectionne oklm
        parents = [
            scoreIndividus[k][0]
            for k in range(
                0,
                int(
                    self.POURCENTAGE_CONSERVATION_FORT * self.TAILLE_POPULATION
                ),
            )
        ]

        # On va prendre quelques autres indidividus histoire d'avoir un peu de diversité
        for individu in [
            scoreIndividus[k][0]
            for k in range(
                int(
                    self.POURCENTAGE_CONSERVATION_FORT * self.TAILLE_POPULATION
                ),
                len(scoreIndividus),
            )
        ]:
            if random() < self.CHANCE_SURVIE_FAIBLE:
                parents.append(individu)

        # MUTATION

        # Il s'agirait ici de faire la mutation
        for individu in parents:
            if random() < self.CHANCE_DE_MUTATION:
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
                            indiceFilsEnlevé = random.randint(
                                0, nombreFils - 1
                            )
                            noeudChoisi.fils.remove(indiceFilsEnlevé)
                        else:
                            taille = len(noeudChoisi.fils)
                            indice_ajout = random.randint(0, taille)
                            noeudChoisi.ajoutFils(
                                Feuille(individu), indice_ajout
                            )

        # CROSSOVER
        nombreParents = len(parents)
        populationManquante = self.TAILLE_POPULATION - nombreParents
        enfants = []

        while len(enfants) < populationManquante:
            # On choisit on hasard le père et la mère
            indexPere = random.randint(0, self.TAILLE_POPULATION - 1)
            indexMere = indexPere
            while indexMere == indexPere:
                indexMere = random.randint(0, self.TAILLE_POPULATION - 1)
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
                nombreFils = (
                    len(petitPere.fils) + len(petiteMere.fils)
                ) // 2
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
            objectif = self.objectif,
            numeroGeneration=1
        )
        i = 1
        meilleurScore = 2 * self.objectif
        while (i < self.GENERATION_MAX) & abs(
            meilleurScore
        ) > self.objectif:
            [
                Generation,
                DistributionScore,
                TemperatureMeilleurArbre,
            ] = Generation.ameliorerPopulation()
            Generation.numeroGeneration += 1
            meilleurScore = abs(DistributionScore[0])
            i += 1
        return Generation[0], DistributionScore[0], TemperatureMeilleurArbre[0]
