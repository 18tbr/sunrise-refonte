import sklearn
import joblib
from operator import itemgetter
import random

sudo python setup.py install

Text
Tint
Pint

class Genetique(object):
    """docstring for Genetique."""

    def __init__(self, args, parametres, sorties, experience):
        super(Genetique, self).__init__()
        # Les arguments de l'experience
        self.args = args
    
    % Roulette wheel selection - plus l'arbre considéré renvoie une température proche de Tint, plus il a de chance d'être sélectionné
    % N_gardé  nombre de grille que l'on conserve
    % Fonction simulation(grille, Text, Pint) retourne Texp la température selon l'arbre de la grille considéré 
    % apply_function calcul l'aire est la courbe de la température intérieure réelle et celle selon l'arbre de la grille considéré
    % fitness_function peut-être 1/apply_function (je sais pas trop en vrai)
    % individus : attribut de Genetique, liste de Grilles
    
    def selection(self, N_gardé):
        % Liste [
        Texp=[[]]
        for v in self.individus :
            diff = apply_function((simulation(v,Text,Pint))
            Texp.append([diff, fitness_function(diff), v])
        
        s = 0
        T = sorted(Texp, key=itemgetter(0))
        for w in Texp :
            s = s + w[1]
        
        Tselected = [[]]
        for j in range(N_gardé) :
            accumulated = 0
            rand = random.uniform(0,1)
            ct = -1
            while rand < accumulated :
                ct = ct +1
                probability = T[ct][1] / s
                accumulated = accumulated + probability
            Tselected.append(T[ct])
                