import numpy as np


def remplirZone(image,couche, NW, SE, val):
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
    image[NW_h:SE_h, NW_w:SE_w,couche ] = val
    

def creerMultiCanal(image, racine, numRacine, NW, SE, profondeur):
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
        remplirZone(image,0, NW, SE, racine.val)
        remplirZone(image,2, NW, SE, profondeur)
    # else...
    else:
        print(f"Noeud")
        for num_fils, fils in enumerate(racine.fils):
            total_fils = len(racine.fils)
            if type(racine) is Serie:  # on divise verticalement
                # new north west
                new_NW_h = NW_h
                new_NW_w = NW_w + (SE_w - NW_w) * num_fils // total_fils
                # new south east
                new_SE_h = SE_h
                new_SE_w = NW_w + (SE_w - NW_w) * (num_fils + 1) // total_fils
                # Capacity north west
                NW_C_h = new_NW_h
                NW_C_w =int((new_NW_w+4*new_SE_w)/5)
                NW_C=( NW_C_h, NW_C_w)
                # Capacity south east
                SE_C_h=new_SE_h
                SE_C_w=int((-new_NW_w+6*new_SE_w)/5)
                SE_C=(SE_C_h,SE_C_w)
                if num_fils+1<total_fils:
                    remplirZone(image,1, NW_C, SE_C, racine.capacites[num_fils])
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
            creerMultiCanal(image, fils, num_fils, new_NW, new_SE, profondeur + 1)

def moyenneZone(image, couche, NW, SE):
    "Donne la moyenne des valeurs d'un condensateur ou d'une résistance sur une zone donnée"
    NW_h, NW_w = NW
    SE_h, SE_w = SE
    return np.mean(image[NW_h:SE_h, NW_w:SE_w,couche ])

def updaterRacine(image, racine, numRacine, NW, SE, profondeur):
    """
    Fonction récursive de mise à jour de la racine de l'arbre.

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
        racine.val=moyenneZone(image,0, NW, SE)
        print(f"Feuille de valeur {racine.val}")
    # else...
    else:
        print(f"Noeud")
        for num_fils, fils in enumerate(racine.fils):
            total_fils = len(racine.fils)
            if type(racine) is Serie:  # on divise verticalement
                # new north west
                new_NW_h = NW_h
                new_NW_w = NW_w + (SE_w - NW_w) * num_fils // total_fils
                # new south east
                new_SE_h = SE_h
                new_SE_w = NW_w + (SE_w - NW_w) * (num_fils + 1) // total_fils
                # Capacity north west
                NW_C_h = new_NW_h
                NW_C_w =int((new_NW_w+4*new_SE_w)/5)
                NW_C=( NW_C_h, NW_C_w)
                # Capacity south east
                SE_C_h=new_SE_h
                SE_C_w=int((-new_NW_w+6*new_SE_w)/5)
                SE_C=(SE_C_h,SE_C_w)
                if num_fils+1<total_fils:
                    racine.capacites[num_fils]=moyenneZone(image,1,NW_C,SE_C)
            else:  # on divise horizontalement
                # north west
                new_NW_h = NW_h + (SE_h - NW_h) * num_fils // total_fils
                new_NW_w = NW_w
                # south east
                new_SE_w = SE_w
                new_SE_h = NW_h + (SE_h - NW_h) * (num_fils + 1) // total_fils
            new_NW = (new_NW_h, new_NW_w)
            new_SE = (new_SE_h, new_SE_w)
            #appel récursif
            racine.fils=updaterRacine(racine=racine.fils,
                                         numRacine=num_fils,
                                         NW=new_NW,
                                         SE=new_SE,
                                         profondeur=profondeur+1,
                                         image=image)
    
    return racine