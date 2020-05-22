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
    BIAIS_ALTERNANCE = 0.2  # Le biai d'alternace est un biai qui pousse l'algorithme de création à créer des arbres avec une alternance de Serie/Parallele pour avoir des solutions plus intéressantes. Il doit être entre 0 (pas de biais d'alternance) et 0.5 (alternance forcée).

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
        # La taille de la population à créer et à faire évoluer
        self.taillePopulation = taillePopulation
        # Le nombre maximal d'itération de l'algorithme
        self.generationMax = generationMax

        # On initialise directement la population à partir du constructeur
        self.populationAleatoire()

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
        # Une graine qui détermine si l'alternance devrait commencre par des liaisons séries ou parallèles. graineAlternance peut prendre les valeurs -Genetique.BIAIS_ALTERNANCE ou Genetique.BIAIS_ALTERNANCE.
        graineAlternance = Genetique.BIAIS_ALTERNANCE + 2 * (random.random() > 0.5) * Genetique.BIAIS_ALTERNANCE
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
                    # Hasard a 50% d'être vrai (et 50% d'être faux) et nous permet de choisir entre ajouter un fils en série et en parallèle. La graineAlternance permet de favoriser tantôt les liaisons séries, tantôt les liaisons parallèles.
                    hasard = random.random() > (0.5 + graineAlternance)
                    if hasard:
                        parent.ajoutFils(enfant, forme="serie")
                    else:
                        parent.ajoutFils(enfant, forme="parallele")
                else:
                    # On tire aléatoirement l'index où l'on va insérer le nouvel enfant parmi les enfants préexistants du parent. Le +1 correspond au fait que l'on peut insérer un enfant tout à la fin de la liste des descendants du parent.
                    indexAleatoire = random.randrange(len(parent.fils) + 1)
                    # On insère le nouvel enfant
                    parent.ajoutFils(enfant, index=indexAleatoire)
            # On alterne le biais entre liaisons séries et parallèle
            graineAlternance *= -1

        # On renvoie la liste ainsi formée
        return individu

    def selection(self):
        # Réduit la population pour n'en conserver que les meilleurs individus
        scoreIndividus = self.scorePopulation()

        # Le rang au dela duquel un individu dans la population est forcémentconservé
        seuilSurvie = self.taillePopulation - int(
            Genetique.POURCENTAGE_CONSERVATION_FORT * self.taillePopulation
        )
        # On sélectionne les meilleurs individus dans la population
        parents = scoreIndividus[seuilSurvie:]

        # Afin d'éviter de tomber dans des minimas locaux trop rapidement, on va faire survivre quelques individus faibles. On crée une liste dédiée pour que le dernier élément de la liste renvoyée à la fin de cette fonction soit bien le meilleur individu de la génération (ce qui n'est pas le cas si on fait directement un parent.append).
        faiblesSurvivants = []
        for individu in scoreIndividus[:seuilSurvie]:
            if random.random() < Genetique.CHANCE_SURVIE_FAIBLE:
                faiblesSurvivants.append(individu)

        parents = faiblesSurvivants + parents
        return [list(i) for i in zip(*parents)]

    # Pour l'instant on utilise un taux de mutation constant
    def mutation(self):
        for individu in self.population:
            # On peut muter un même individu plusieurs fois si le hasard le veux
            while random.random() < Genetique.CHANCE_DE_MUTATION:
                profondeur = len(individu.forme)
                # On tire une profondeur à laquelle faire la mutation
                choixProfondeur = random.randrange(profondeur)
                # Le nombre de noeuds à la profondeur donnée
                largeur = individu.forme[choixProfondeur]
                # On choisit un individu au hasard parmi ceux à cette profondeur
                choixLargeur = random.randrange(largeur)
                # On récupère l'individu tiré au hasard
                noeud = individu.inspecter(choixProfondeur, choixLargeur)

                # On tire aléatoirement entre True et False avec équiprobabilité
                action = random.random() > 0.5

                # L'action sera différente si le noeud tiré est une Feuille ou non.
                if type(noeud) is Feuille:
                    # On va ajouter une feuille à ce noeud
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
                        # 50% de chances d'ajouter un enfant
                        # On tire un indice sur le lequel faire notre action dans 0, nombreFils inclu
                        choixIndex = random.randrange(nombreFils+1)
                        fils = Feuille()
                        noeud.ajoutFils(fils, index=choixIndex)
                    else:
                        # 50% de chances de supprimer un fils
                        # On tire un indice sur le lequel faire notre action dans 0, nombreFils exclu
                        choixIndex = random.randrange(nombreFils)
                        noeud.suppressionFils(index=choixIndex)

    def fusion(self):
        # On ajoutera tous les enfants d'un seul coup à la fin pour éviter de faire une fusion sur un enfant qui vient d'être créé.
        enfants = []
        # On calcule le nombre d'individus qu'il nous reste à produire pour compléter la génération suivante.
        populationManquante = self.taillePopulation - len(self.population)
        for i in range(populationManquante):
            # On tire deux individus dans la population sans faire de remise.
            pere, mere = random.sample(self.population, k=2)

            # Il nous faut à présent déterminer la profondeur maximale jusqu'à laquelle les deux parents ont une forme commune.
            profondeurSemblable = 0
            # On teste toutes les profondeurs et on s'arrète à la première non commune
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
            # On tire au hasard le parent dont on va récupérer le sommet
            choixSommet = random.random() > 0.5
            if choixSommet:
                sommet = mere.racine.sousArbre()
            else:
                sommet = pere.racine.sousArbre()

            # On crée l'objet Grille qui acueille le sommet. Le constructeur de grille dispose d'une syntaxe spéciale concue pour attacher une racine direcetement.
            enfant = Grille(self.Cint, self.T, self.Text, self.Tint, self.Pint, racine=sommet)

            # Le nombre de noeuds qui vont devoir être fusionnés entre parent et enfant.
            largeur = enfant.forme[profondeurSemblable]
            # On réalise l'étape de fusion pour tous les noeuds de profondeurSemblable
            for j in range(largeur):
                # On récupère le noeud correspondant pour la mere, le pere et l'enfant
                noeudPere = pere.inspecter(profondeurSemblable, j)
                noeudMere = mere.inspecter(profondeurSemblable, j)
                noeudEnfant = enfant.inspecter(profondeurSemblable, j)
                # On crée la liste de tous les nouveaux enfants possibles.
                # Un détail d'implémentation : en théorie on devrait faire un choix parmi les sousArbre crées à partir des enfants de pere et mere, mais créer un sousArbre peut être un peu long, donc en créer qui ne seront pas utilisés est une perte de temps. Au lieu de cela, on va faire notre choix sur les enfants directs de pere et mere, puis calculer le sousArbre des enfants élus, ce qui est plus efficace mais amène au même résultat.
                if type(noeudEnfant) is Feuille:
                    # Si on tombe sur une feuille, on ne peut évidemment pas y ajouter de fils.
                    continue
                filsPotentiels = noeudPere.fils + noeudMere.fils
                # On détermine le nombre d'enfants à donner à l'enfant.
                nombreFils = len(filsPotentiels) // 2 + 1
                # On choisit nombreFils éléments parmi filsPotentiels sans remise.
                filsChoisis = random.sample(filsPotentiels, k=nombreFils)
                # On calcule le sousArbre des enfants choisis avant de l'ajouter à l'enfant.
                sousArbresChoisis = [fils.sousArbre() for fils in filsChoisis]
                # Enfin, on ajoute les nouveaux sous arbres créés sous le noeud choisi de enfant.
                noeudEnfant.substituerEnfants(sousArbresChoisis)
            # On ajoute la grille créée à la population de descendants
            enfants.append(enfant)
        # On renvoie la liste des enfants créés pour qu'ils soient ajoutés à la population
        return enfants

    # Effectue une génération de l'algorithme génétique et renvoie queleques valeurs qui sont utiles pour l'affichage.
    def ameliorerPopulation(self):

        # SELECTION
        print("Selection")
        self.population, scores = self.selection()

        # On crée une copie du meilleur individu de la génération (il risque d'être modifié par mutation)
        meilleurArbre = self.population[-1].racine.sousArbre()
        meilleurIndividu = Grille(self.Cint, self.T, self.Text, self.Tint, self.Pint, racine=meilleurArbre)

        # MUTATION
        print("Mutation")
        self.mutation()

        # FUSION
        print("Fusion")
        self.population += self.fusion()

        # On renvoie des valeurs qui pourront être utiles pour l'affichage (le meilleur individu, )
        return meilleurIndividu, scores[-1]


    # Réalise l'optimisation de la population par l'algorithme génétiques. Il s'agit d'une fonction génératrice qui "yield" (cède, je crois) les valeurs intéressantes pour l'animation de l'interface graphique à chaque génération. Une fois l'algorithme terminé, le résultat de l'algorithme est contenu dans les différents attributs de l'objet.
    def optimisation(self):
        generation = 0
        meilleurScore = 2 * self.objectif
        while (generation < self.generationMax) and (abs(meilleurScore) > self.objectif):
            meilleurIndividu, meilleurScore = self.ameliorerPopulation()
            generation += 1
            yield generation, meilleurIndividu, meilleurScore
