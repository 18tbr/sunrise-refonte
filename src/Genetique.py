from operator import itemgetter  # Permettre de trier des listes
import random  # Permettre d'introduire du hasard


class Genetique(object):
    """docstring for Genetique."""

    def __init__(self, cint, T, Text, Tint, Pint, numeroGeneration):
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

        self.numeroGeneration = numeroGeneration

        # ATTENTION
        # A revoir peut-être après avoir visionné la vidéo
        self.PROFONDEUR_MAX_ARBRE = 100
        self.LARGEUR_MAX_ARBRE = 50
        self.NOMBRE_FILS_MAX_ARBRE = 5

        self.CHANCE_DE_MUTATION = 0.1
        self.POURCENTAGE_CONSERVATION_FORT = 0.2  # Pourcentage de la population qui va être gardé la génération suivante, les meilleurs individus
        self.CHANCE_SURVIE_FAIBLE = 0.05  # Pourcentage de la population qui va être gardé la génération suivante, bien que ne figurant pas parmis les meilleurs individus
        self.TAILLE_POPULATION = 100
        self.GENERATION_MAX = 100000

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

        individu.racine = Feuille(individu)

        individu.forme = [1]

        for i in range(profondeur - 1):
            # On détermine au hasard la largeur de la généation suivante
            largeur = random.randint(1, self.LARGEUR_MAX_ARBRE)

            # On répartit les différents éléments sur les différents indices
            liste_indices = [k for k in range(0, largeur)]
            indices_choisis = random.choices(
                liste_indices, k=(individu.forme[i] - 1)
            )
            indices_choisis.append(0)
            indices_choisis.append(individu.forme[i] - 1)
            indices_choisis.sort()

            # on créé alors le nombre de fils correspondant
            for k in range(individu.forme[i] - 1):
                parent = inspecter(individu, i, k)
                n_fils = indices_choisis[k + 1] - indices_choisis[k]
                if n_fils > 0:
                    hasard = random.randint(1, 2)
                    if hasard == 1:
                        parent.ajoutFils(individu, forme="serie")
                        # A VOIR
                        # Non, là parent continue d'être la feuille que tu avais inspectée au début. Je vais modifier la fonction ajoutFils pour que tu puisses faire cela plus facilement.
                        for j in range(n_fils):
                            parent.ajoutFils(individu, index=j)
                    else:
                        parent.ajoutFils(individu, forme="parallel")
                        # A VOIR
                        # Non, là parent continue d'être la feuille que tu avais inspectée au début. Je vais modifier la fonction ajoutFils pour que tu puisses faire cela plus facilement.
                        for j in range(n_fils):
                            parent.ajoutFils(individu, index=j)

    def enleverFilsAleatoire(self, individual, profondeur, indice):
        noeudChoisi = individual.inspecter(profondeur, indice)
        taille = len(noeudChoisi.fils)
        for i in range(taille):
            hasard = random.randint(0, 1)
            if hasard:
                noeudChoisi.suppressionFils(i)

    def ajoutFilsAleatoire(self, individu, cas, profondeur, indice):
        # cas = 2 ou 3 (2 --> il faut absolument un fils, 3 --> on peut avoir le cas où il n'y en a pas)

        parent = individu.inspecter(profondeur, indice)

        format = random.randint(1, cas)
        # On détermine le nombre de fils (oui ça sert à rien si format ==3)
        nombreFils = random.randint(1, self.NOMBRE_FILS_MAX_ARBRE)
        if format == 1:
            parent.ajoutFils(Feuille(individu), forme="serie")
            # Non, là parent continue d'être la feuille que tu avais inspectée au début. Je vais modifier la fonction ajoutFils pour que tu puisses faire cela plus facilement.
            for j in range(nombreFils):
                parent.ajoutFils(Feuille(individu), index=j)
        if format == 2:
            parent.ajoutFils(Feuille(individu), forme="parallele")
            # Même problème que pour série
            for j in range(nombreFils):
                parent.ajoutFils(Feuille(individu), index=j)

    # Fonction qui va faire évoluer la population d'une génération à une autre
    # Sélection
    # Mutation
    # Fusion

    def ameliorerPopulation(self):

        # SELECTION
        scoreIndividus = self.scorePopulation()

        # On a les meilleurs individus qu'on sélectionne oklm
        parents = scoreIndividus[
            : int(self.POURCENTAGE_CONSERVATION_FORT * self.TAILLE_POPULATION)
        ]

        # On va prendre quelques autres indidividus histoire d'avoir un peu de diversité
        for individu in scoreIndividus[
            int(self.POURCENTAGE_CONSERVATION_FORT * self.TAILLE_POPULATION) :
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
                            self.ajoutFilsAleatoire(
                                individu, 3, profondeur, indice
                            )

                    else:
                        if action == 0:
                            self.enleverFils(individu, profondeur, indice)
                        else:
                            taille = len(noeudChoisi.fils)
                            nombreAjouts = random.randint(
                                0, self.NOMBRE_FILS_MAX_ARBRE - taille
                            )
                            for j in range(n_ajout):
                                noeudChoisi.ajoutFils(
                                    Feuille(individual),
                                    random.randint(0, taille + nombreAjouts),
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
            enfant.racine = pere.racine
            # Vérifier les dépendances, j'ai un vieux doute.

            for j in range(pere.forme[i]):
                petit_pere = inspecter(pere, i, j)
                petite_mere = inspectr(mere, i, j)
                fils_potentiels = petit_pere.fils + petit_pere.fils
                nombre_fils = (len(petit_pere.fils) + len(petit_pere.fils)) // 2
                fils_choisis = random.choices(fils_potentiels, k=nombre_fils)
                substituerEnfants(enfant, fils_choisis)

            # La population de la génération suivante
            self.population = parents + children
