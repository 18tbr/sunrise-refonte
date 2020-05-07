import numpy as np


def remplirZone(image, NW, SE, val):
    """
    Colorie une zone de l'image.

    Parameters
    ----------
    image : numpy array
        Image to fill.
    NW = (NW_h, NW_w) : (int, int)
        Coin North-West de la portion de l'image.
    SE = (SE_h, SE_w) : (int, int)
        Coin South-East de la portion de l'image.
    val : int
        Valeur avec laquelle colorier la portion d'image.
    """
    print(f"On colorie de {NW} à {SE}")
    NW_h, NW_w = NW
    SE_h, SE_w = SE
    image[NW_h:SE_h, NW_w:SE_w] = val


def creerCanalResistance(image, racine, numRacine, NW, SE, profondeur):
    """
    Fonction récursive de création du canal résistance de l'arbre.

    Parameters
    ----------
    image : numpy array
        Image to modify.
    racine : Noeud
    numRacine : int
        Numéro de la racine parmi les fils de son père.
    NW = (NW_h, NW_w) : (int, int)
        Coin North-West de la portion de l'image.
    SE = (SE_h, SE_w) : (int, int)
        Coin South-East de la portion de l'image.
    profondeur : int
        Profondeur de racine, utile pour savoir si l'on divise
        verticalement ou horizontalement.
        On alterne le sens de division, et on commence par une
        division verticale.

    """
    # get coord
    NW_h, NW_w = NW
    SE_h, SE_w = SE
    # cas de base
    if type(racine) is Feuille:
        print(f"Feuille de valeur {racine.val}")
        remplirZone(image, NW, SE, racine.val)
    # else...
    else:
        print(f"Noeud")
        for num_fils, fils in enumerate(racine.fils):
            total_fils = len(racine.fils)
            if type(racine) is Serie:  # on divise verticalement
                # north west
                new_NW_h = NW_h
                new_NW_w = NW_w + (SE_w - NW_w) * num_fils // total_fils
                # south east
                new_SE_h = SE_h
                new_SE_w = NW_w + (SE_w - NW_w) * (num_fils + 1) // total_fils
            else:  # on divise horizontalement
                # north west
                new_NW_h = NW_h + (SE_h - NW_h) * num_fils // total_fils
                new_NW_w = NW_w
                # south east
                new_SE_w = SE_w
                new_SE_h = NW_h + (SE_h - NW_h) * (num_fils + 1) // total_fils
            new_NW = (new_NW_h, new_NW_w)
            new_SE = (new_SE_h, new_SE_w)
            # appel résursif
            creerCanalResistance(image, fils, num_fils, new_NW, new_SE, profondeur + 1)


def creerCanalCapacite(image, racine, numRacine, NW, SE, profondeur):
    """
    Fonction récursive de création du canal capacité de l'arbre.

    Parameters
    ----------
    image : numpy array
        Image à modifier.
    racine : Noeud
    numRacine : int
        Numéro de la racine parmi les fils de son père.
    NW = (NW_h, NW_w) : (int, int)
        Coin North-West de la portion de l'image.
    SE = (SE_h, SE_w) : (int, int)
        Coin South-East de la portion de l'image.
    profondeur : int
        Profondeur de racine, utile pour savoir si l'on divise
        verticalement ou horizontalement.
        On alterne le sens de division, et on commence par une
        division verticale.

    """
    return None  # to do
