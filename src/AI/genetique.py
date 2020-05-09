from operator import itemgetter     # Indiquer ici à quoi cet import sert dans le code (en quelques mots)
import random   # idem


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

        # A revoir peut-être après avoir visionné la vidéo
        self.PROFONDEUR_MAX_ARBRE = 100
        self.NOMBRE_FILS_MAX_ARBRE = 5

        self.CHANCE_DE_MUTATION = 0.1
        self.POURCENTAGE_CONSERVATION_FORT = 0.2    # Détailler à quoi cette variable sert ici
        self.CHANCE_SURVIE_FAIBLE = 0.05     # Détailler ici à quoi sert cette variable
        self.TAILLE_POPULATION = 100
        self.GENERATION_MAX = 100000


    # (TBR) : Etrange de passer la population en argument si elle vaut toujours self.population...
    def scorePopulation(self, population):
        # Calcule le score de la population, renvoie une liste de doublet (individu, score) triée par score sur toute la population. Les individus avec le meilleur score sont au début.
        scoreIndividus = []
        for individu in population:
            scoreIndividus.append((individu, individu.score()))
        return sorted(scoreIndividus, key=itemgetter(1), reverse=True)



#def selection(self):
    # % Roulette wheel selection - plus l'arbre considéré renvoie une température proche de Tint, plus il a de chance d'être sélectionné
    # % N_gardé  nombre de grille que l'on conserve
    # % Fonction simulation(grille, Text, Pint) retourne Texp la température selon l'arbre de la grille considéré
    # % apply_function calcul l'aire est la courbe de la température intérieure réelle et celle selon l'arbre de la grille considéré
    # % fitness_function peut-être 1/apply_function (je sais pas trop en vrai)
    # % individus : attribut de Genetique, liste de Grilles
        # % Liste [
        # Texp=[[]]
        # for v in self.individus :
        #     diff = apply_function((simulation(v,Text,Pint))
        #     Texp.append([diff, fitness_function(diff), v])
        #
        # s = 0
        # T = sorted(Texp, key=itemgetter(1))
        # for w in Texp :
        #     s = s + w[1]
        #
        # Tselected = [[]]
        # for j in range(N_gardé) :
        #     accumulated = 0
        #     rand = random.uniform(0,1)
        #     ct = -1
        #     while rand < accumulated :
        #         ct = ct +1
        #         probability = T[ct][1] / s
        #         accumulated = accumulated + probability
        #     Tselected.append(T[ct])

    # Methode de sélection simple, on va juste prendre les meilleurs en mode oklm.
    def ameliorerPopulation(self):
        scoreIndividus = self.scorePopulation(self.population)

        #On a les meilleurs individus qu'on sélectionne oklm
        parents = scoreIndividus[:int(self.POURCENTAGE_CONSERVATION_FORT * self.TAILLE_POPULATION)]

        #On va prendre quelques autres indidividus histoire d'avoir un peu de diversité
        for individu in scoreIndividus[int(self.POURCENTAGE_CONSERVATION_FORT * self.TAILLE_POPULATION):]:
            if random() < self.CHANCE_SURVIE_FAIBLE:
                parents.append(individu)

        #Il s'agirait ici de faire la mutation
        for individu in parents:
            if random() < self.CHANCE_DE_MUTATION:
                # individu va être modifié
                forme = individu.forme
                #choix totalement arbitraire selon mon humeur - à revoir !!!!!!
                nombreModifications = random.randint(1, len(forme))
                for i in range(nombreModifications) :
                    profondeur = random.randint(0, len(forme)-1)
                    indice = random.randint(0, forme[i]-1)
                    noeudChoisi = individual.inspecter(profondeur, indice)
                    #Vision du monde manichéenne, soit optique de rajouter du nouveau (1), soit de supprimer (0)
                    # (TBR) Ce n'est pas ce que tu fais vraiment
                    action = random.randint(0,1)

                    if type(noeudChoisi) == Feuille :
                        # On modifie la valeur de la résistance, mais bon ils sont pas clairs niveau argument donc à revoir !!!
                        # (TBR) La valeur que tu veux modifier est H = 1/R. Val n'existe pas et va être supprimé.
                        if action == 0:
                            # (TBR) Cet aléa est arbitraire, il faudra le modifier plus tard.
                            noeudChoisi.val = random.randint(0, 42)
                        else:
                            self.ajoutFilsAleatoire(individu, 3, profondeur, indice)

                    else:
                        if action == 0 :
                            self.enleverFils(individu, profondeur, indice)
                        else :
                            taille = len(noeudChoisi.fils)
                            nombreAjouts = random.randint(0, self.NOMBRE_FILS_MAX_ARBRE-taille)
                            for j in range(n_ajout) :
                                noeudChoisi.ajoutFils(Feuille(individual), random.randint(0,taille+nombreAjouts))


        #Il s'agirait ici de faire les crossover

        #Pour l'instant en mode très basique, on va juste prendre un élément au hasard du père qu'on va supprimer tout les fils à partir de ce noeuf, prendre un élément au hasard de la mère et sélectionner toute sa descendance et hop on fusionner les deux
        #Oui cross over pourri.
        #Déjà voir si on pourrait pas garder une partie de la descendance

        nombreParents = len(parents)
        populationManquante = self.TAILLE_POPULATION - nombreParents
        enfants = []
        while len(enfants) < populationManquante:
            # Bref on choisit on hasard le père et la mère
            indexPere = random.randint(0, self.TAILLE_POPULATION-1)
            # (TBR) Tu devrais plutôt choisir un individu au hasard ici même si tu vas rentrer dans la boucle plus tard.
            indexMere = indexPere
            while indexMere == indexPere :
                indexMere = random.randint(0, self.TAILLE_POPULATION-1)
            # (TBR) Je crois que la syntaxe que tu cherches est "self.population[indexPere]"...
            pere = self.population(indexPere)
            mere = self.population(indexPere)
            #A FAIRE ENVISAGER PLUS DE PARITE, ON CHANGE LES ROLES AVEC UNE VARIABLE ALEATOIRE
            # PAS IMPLEMENTER, SERT A R
            profondeurPere = random.randint(0, len(pere.forme) -1)
            indicePere = random.randint(0, pere.forme[profondeurPere]-1)
            #Jpense qu'il est inutile en fait, dépend de la fnction de Ouk
            dechuPere = pere.inspecter(profondeurPere, indicePere)

            profondeurMere = random.randint(0, len(mere.forme) -1)
            indiceMere = random.randint(0, mere.forme[profondeurMere]-1)
            eluMere = mere.inspecter(profondeurMere, indiceMere)

            fils = Grille(self.cint, self.T, self.Text, self.Tint, self.Pint)
            hautArbre = pere.fonctionOukHautArbre(dechuPere)
            basArbre = mere.sousArbre()
            # (TBR) Une grille n'a pas d'attribut noeud !!
            # (TBR) Est-ce que tu veux parler de fils.racine ?
            fils.noeud = hautArbre.noeud
            # (TBR) Non, utiliser ajouter fils. Cela ne marchera pas.
            fils.inspecter(profondeurPere, indicePere) = basArbre.noeud
            # (TBR) En dehors du fait que l'algorithme de fusion que tu proposes ne semble pas fonctionner (ce n'est pas très grave, c'est un bon début qui t'aidera à comprendre celui que je te propose), tu n'ajoutes jamais fils à enfant. Le principal problème dans ton algorithme est que tu essaies de concatener les arbres (comme tu le ferais avec des listes), mais ce n'est pas comme cela qu'un arbre se présente.

    #A verif cette partie 6- IMPORTANT - IMPORTANT - IMPORTANT


    #La population de la génération suivante
    # (TBR) Tu ne renvoies rien à la fin de cette fonction. Est-ce que tu essaies de dire "self.population = parents + enfants" ?
    parents.extend(children)







    def populationAleatoire(self) :
        population = []
        for i in range(self.TAILLE_POPULATION) :
            population.append(self.individuAleatoire())
        # (TBR) Pourquoi ne pas modifier self.population directement alors ?
        self.population = population


    # (TBR) L'implémentation de cette fonction est étrange, je ne suis pas certain qu'elle fonctionne.
    def individuAleatoire(self):
        profondeur = random.randint(1, self.PROFONDEUR_MAX_ARBRE)
        individu = Grille(self.cint, self.T, self.Text, self.Tint, self.Pint)
        #Série (1) / Parallèle (2) / Rien (3)

        # (TBR) noeud n'existe pas, ce que tu cherches s'appelle racine je pense.
        # (TBR) Qu'est-ce que cette ligne est censée faire ? Détaille le s'il te plait, la syntaxe n'est pas évidente à lire.
        individu.noeud = Feuille(individu)
        #A verif avec OUK, on n'est pas d'accord !!!!!!!!!!!!!
        #ATTENTION!!!!!!!!!!!!!!!!
        individu.forme = [1] ;

        for i in range(profondeur-1):
            #Il faut qu'il y ait au moins un fils
            nombreParents = individu.forme[i]
            #On détermine l'indice où il y aura forcément un fils
            indiceDescendanceSure = random.randint(1, nombreParents)
            self.ajoutFilsAleatoire(individu, 2, i, indiceDescendanceSure)
            #Pour les autres, ils peuvent ne pas avoir de fils
            for k in range(1, nombreParents):
                if k != indiceDescendanceSure :
                    self.ajoutFilsAleatoire(individu, 3, i, k)

    def enleverFilsAleatoire(self, individual, profondeur, indice) :
        noeudChoisi = individual.inspecter(profondeur, indice)
        taille = len(noeudChoisi.fils)
        for i in range(taille) :
            hasard = random.randint(0,1)
            if hasard == 0 :    # (TBR) "if hasard:" plutôt, non ?
                noeudChoisi.suppressionFils(i)


    def ajoutFilsAleatoire(self, individu, cas, profondeur, indice) :
        #cas = 2 ou 3 (2 --> il faut absolument un fils, 3 --> on peut avoir le cas où il n'y en a pas)
        # (TBR) Parce que mettre un argument appelé "doitAvoirFils" qui puisse prendre les valeur True ou False c'est clairement surfait...
        parent = individu.inspecter(profondeur, indice)

        # (TBR) type est un mot clef reservé en python, trouve un autre nom pour ta variable
        type = random.randint(1,cas)
        #On détermine le nombre de fils (oui ça sert à rien si type ==3)
        nombreFils = random.randint(1, self.NOMBRE_FILS_MAX_ARBRE)
        if type == 1 :
            parent.ajoutFils(Feuille(individu), forme = 'serie')
            # Non, là parent continue d'être la feuille que tu avais inspectée au début. Je vais modifier la fonction ajoutFils pour que tu puisses faire cela plus facilement.
            for j in range(nombreFils) :
                parent.ajoutFils(Feuille(individu), index = j)
        if type == 2 :
            parent.ajoutFils(Feuille(individu), forme = 'parallele')
            # Même problème que pour série
            for j in range(nombreFils):
                parent.ajoutFils(Feuille(individu), index = j)
