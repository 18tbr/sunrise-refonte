
from operator import itemgetter
import random




class Genetique(object):
    """docstring for Genetique."""

    def __init__(self, cint, T, Text, Tint, Pint,numero_Generation ):
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
        
        self.numero_Generation = numero_Generation
        
        self.PROFONDEUR_MAX_ARBRE = 100
        self.NOMBRE_FILS_MAX_ARBRE = 5
        
        self.CHANCE_TO_MUTATE = 0.1
        self.GRADED_RETAIN_PERCENT = 0.2
        self.CHANCE_RETAIN_NONGRATED = 0.05
        self.POPULATION_COUNT = 100
        self.GENERATION_COUNT_MAX = 100000
        

        

    def graded_population(self, population):
    #Grade the population. Return a list of tuple (individual, fitness) sorted from most graded to less graded. """
        graded_individual = []
        for individual in population :
            graded_individual.append( (individual, individual.score() ) )
        return sorted(graded_individual, key=itemgetter(1), reverse=True)


    
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

    def evolve_population(self):
        graded_population = graded_population(self.population)
        
        
# Methode de sélection simple, on va juste prendre les meilleurs en mode oklm.
    
        
    #On a les meilleurs individus qu'on sélectionne oklm
        parents = graded_population[:int(self.GRADED_RETAIN_PERCENT * self.POPULATION_COUNT)]
    
    #On va prendre quelques autres indidividus histoire d'avoir un peu de diversité
        for individual in graded_population[int(self.GRADED_RETAIN_PERCENT * self.POPULATION_COUNT):]:
            if random() < self.CHANCE_RETAIN_NONGRATED:
                parents.append(individual)
        
#Il s'agirait ici de faire la mutation

        for individual in parents:
            if random() < self.CHANCE_TO_MUTATE:
                # individu va être modifié
                forme = individual.forme
                #choix totalement arbitraire selon mon humeur - à revoir !!!!!!
                n_modification = random.randint(1, len(forme))
                for i in range(n_modification) :
                    profondeur = random.randint(0, len(forme)-1)
                    indice = random.randint(0, forme[i]-1)
                    noeud_choisi = individual.inspecter(profondeur, indice)
                    #Vision du monde manichéenne, soit optique de rajouter du nouveau (1), soit de supprimer (0)
                    action = random.randint(0,1)
                    
                    if type(noeud_choisi) == Feuille :
                        # On modifie la valeur de la résistance, mais bon ils sont pas clairs niveau argument donc à revoir !!!
                        if action == 0 :
                            noeud_choisi.val = random.randint(0, 42)
                        else :
                            self.random_ajout_fils(indivudual, 3, profondeur, indice)
                            
                    else:
                        if action == 0 :
                            self.enlever_fils( individual, profondeur, indice)
                        else :
                            taille = len(noeud_choisi.fils)
                            n_ajout = random.randint(0, self.NOMBRE_FILS_MAX_ARBRE-taille)
                            for j in range(n_ajout) :
                                noeud_choisi.ajoutFils(Feuille(individual), random.randint(0,taille+n_ajout) )
 

#Il s'agirait ici de faire les crossover

#Pour l'instant en mode très basique, on va juste prendre un élément au hasard du père qu'on va supprimer tout les fils à partir de ce noeuf, prendre un élément au hasard de la mère et sélectionner toute sa descendance et hop on fusionner les deux
#Oui cross over pourri.
#Déjà voir si on pourrait pas garder une partie de la descendance

        parents_len = len(parents)
        desired_len = self.POPULATION_COUNT - parents_len
        children = []
        while len(children) < desired_len:
            #Bref on choisit on hasard the father et the mother
            n_father = random.randint(0, self.POPULATION_COUNT-1)
            n_mother = n_father
            while n_mother = n_father :
                n_mother = random.randint(0, self.POPULATION_COUNT-1)
            father = self.population(n_father)
            mother = self.population(n_mother)
            #A FAIRE ENVISAGER PLUS DE PARITE, ON CHANGE LES ROLES AVEC UNE VARIABLE ALEATOIRE
            # PAS IMPLEMENTER, SERT A R
            profondeur_father = random.randint(0, len(father.forme) -1)
            indice_father = random.radint(0, father.forme[profondeur_father]-1)
            #Jpense qu'il est inutile en fait, dépend de la fnction de Ouk
            dechu_father = father.inspecter(profondeur_father, indice_father)
            
            profondeur_mother = random.randint(0, len(motheur.forme) -1)
            indice_mother = random.radint(0, mother.forme[profondeur_mother]-1)
            elu_mother = mother.inspecter(profondeur_mother, indice_mother)

            child = Grille(self.cint, self.T, self.Text, self.Tint, self.Pint) 
            Haut_Arbre = father.fonction_Ouk_Haut_Arbre(dechu_father)
            Bas_Arbre = mother.sousArbre()
            child.noeud = Haut_Arbre.noeud
            child.inspecter(profondeur_father, indice_father) = Bas_Arbre.noeud
            
#A verif cette partie 6- IMPORTANT - IMPORTANT - IMPORTANT

            
#La population de la génération suivante
    parents.extend(children)







    def random_population(self) :
        population = []
        for i in range(self.POPULATION_COUNT) :
            population.append(self.random_individual())
        self.population = population


    def random_individual(self):
        profondeur = random.randint(1, self.PROFONDEUR_MAX_ARBRE)
        individual = Grille(self.cint, self.T, self.Text, self.Tint, self.Pint) 
        #Série (1) / Parallèle (2) / Rien (3)
        
        individual.noeud = Feuille(individual)
        #A verif avec OUK, on n'est pas d'accord !!!!!!!!!!!!!
        #ATTENTION!!!!!!!!!!!!!!!!
        individual.form = [1] ;

        for i in range(profondeur-1):
            #Il faut qu'il y ait au moins un fils
            n_parents = individual.forme[i]
            #On détermine l'indice où il y aura forcément un fils
            n_descendance = random.randit(1, n_parents)
            self.random_ajout_fils(individual, 2, i, n_descendance)
           #Pour les autres, ils peuvent ne pas avoir de fils
            for k in range(1, n_parents):
                if k != n_descendance :
                    self.random_ajout_fils(individual, 3, i, k)
                    
    def enlever_fils(self, individual, profondeur, indice) :
        noeud_choisi = individual.inspecter(profondeur, indice)
        taille = len(noeud_choisi.fils)
        for i in range(taille) :
            hasard = random.randint(0,1)
            if hasard == 0 :
                noeud_choisi.suppressionFils(i)

    
    def random_ajout_fils(self, individual, n_cas, profondeur, indice) :
        #n_cas = 2 ou 3 (2 --> il faut absolument un fils, 3 --> on peut avoir le cas où il n'y en a pas)
        parent = individual.inspecter(profondeur, indice)
        
        type = random.randint(1,n_cas)
        #On détermine le nombre de fils (oui ça sert à rien si type ==3)
        n_fils = random.randint(1, self.NOMBRE_FILS_MAX_ARBRE)
        if type == 1 :
            parent.ajoutFils(Feuille(individual), forme = 'serie')
            for j in range(n_fils) :
                parent.ajoutFils(Feuille(individual), index = j)
        if type == 2 :
                parent.ajoutFils(Feuille(individual), forme = 'parallele')
                for j in range(n_fils) :
                    parent.ajoutFils(Feuille(individual), index = j)