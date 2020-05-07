import sklearn
import joblib
from operator import itemgetter
import random


#Grille.mutate() : une fonction -normalement fait par le groupe Grille - qui engendre une modification aléatoire sur l'arbre

#Simulation.simulation() : une fonction - normalement faite par le groupe Simulation - qui retourne l'évolution de la température pour  l'arbre considéré

class Genetique(object):
    """docstring for Genetique."""

    def __init__(self, Text, Tint, Pint,numeroGeenration ):
        super(Genetique, self).__init__()
        # Liste des individus de la population - chaque individu de type Grille
        self.population = population
        self.Text = Text
        self.Tint = Tint
        self.Pint = Pint
        self.numeroGeneration = numeroGeenration
        self.CHANCE_TO_MUTATE = 0.1
        self.GRADED_RETAIN_PERCENT = 0.2
        self.CHANCE_RETAIN_NONGRATED = 0.05
        self.POPULATION_COUNT = 100
        self.GENERATION_COUNT_MAX = 100000
        

    def fitness(individual)
        fitness = 0 ;
        Texp = Simulation.simulation(individual)
        for t in Texp :
            fitness -= (t-Tint)^2
        return fitness
        

    def graded_population(population):
    #Grade the population. Return a list of tuple (individual, fitness) sorted from most graded to less graded. """
        graded_individual = []
        for individual in self.population :
            graded_individual.append((individual, fitness(individual)))
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

    def evolve_population(population):

# Methode de sélection simple, on va juste prendre les meilleurs en mode oklm.
    
    graded_population = graded_population(population)
    #On a les meilleurs individus qu'on sélectionne oklm
    parents = graded_population[:int(GRADED_RETAIN_PERCENT * POPULATION_COUNT)]
    
    #On va prendre quelques autres indidividus histoire d'avoir un peu de diversité
    for individual in graded_population[int(GRADED_RETAIN_PERCENT * POPULATION_COUNT):]:
        if random() < CHANCE_RETAIN_NONGRATED:
            parents.append(individual)
        
#Il s'agirait ici de faire la mutation
    for individual in parents:
        if random() < CHANCE_TO_MUTATE:
            Grille.mutate(individual)

#Il s'agirait ici de faire les crossover

    return population




        