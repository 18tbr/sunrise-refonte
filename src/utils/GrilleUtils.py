import numpy as np


def remplirZone(image, canal, NW, SE, val):
    """
    Colorie une zone de l'image.

    Parameters
    ----------
    image : numpy array
        Image à remplir.
            canal : int
        Canal cible.
            NW = (NWH, NWW) : (int, int)
        Coin North-West de la portion de l'image.
    SE = (SEH, SEW) : (int, int)
        Coin South-East de la portion de l'image.
    val : int
        Valeur avec laquelle colorier la portion d'image.

    Returns
    -------
    La fonction modifie `image` en place.
    """
    print(f"On colorie le canal {canal} de {NW} à {SE}")
    NWH, NWW = NW
    SEH, SEW = SE
    image[NWH:SEH, NWW:SEW, couche] = val


def creerImage(image, racine, numRacine, NW, SE, profondeur):
    """
    Fonction récursive de création de l'image représentant l'arbre.

    Parameters
    ----------
    image : numpy array
        Image à modifier.
    racine : Grille.Noeud
        Noeud que l'on examine.
    numRacine : int
        Numéro de la racine parmi les fils de son père.
    NW = (NWH, NWW) : (int, int)
        Coin North-West de la portion de l'image.
    SE = (SEH, SEW) : (int, int)
        Coin South-East de la portion de l'image.
    profondeur : int
        Profondeur de racine, stocké pour colorier le 3e canal.

    Returns
    -------
    La fonction modifie `image` en place.

    Notes
    -----
    L'image représentant un arbre possède 3 canaux :
    - le canal 0 contient les valeurs des résistances de l'arbre ;
    - le canal 1 contient les valeurs des capacités de l'arbre ;
    - le canal 2 contient les profondeurs des noeuds de l'arbre.

    A chaque appel récursif, on lit le type du ``Noeud`` sur lequel on
    tombe :
    - si l'on tombe sur une ``Feuille``, on colorie les zones 0 et 2 ;
    - si l'on tombe sur une liaison ``Serie``, on divise l'image
    verticalement et on remplit le canal 1 au passage, puis on
    réalise l'appel récursif ;
    - si l'on tombe sur une liaison ``Parallele``, on divise l'image
    horizontalement et on réalise l'appel récursif.
    """
    # Récupération des coordonnées
    NWH, NWW = NW
    SEH, SEW = SE
    # cas de base
    if type(racine) is Feuille:
        print(f"Feuille de valeur {racine.val}")
        remplirZone(image, 0, NW, SE, racine.val)
        remplirZone(image, 2, NW, SE, profondeur)
    # else...
    else:
        print(f"Noeud")
        for numFils, fils in enumerate(racine.fils):
            totalFils = len(racine.fils)
            if type(racine) is Serie:  # on divise verticalement
                # new north west
                nouvNWH = NWH
                nouvNWW = NWW + (SEW - NWW) * numFils // totalFils
                # new south east
                nouvSEH = SEH
                nouvSEW = NWH + (SEW - NWH) * (numFils + 1) // totalFils
                # capacité north west
                NWCH = nouvNWH
                NWCW = (nouvNWH + 4 * nouvSEW) // 5
                NWC = (NWCH, NWCW)
                # capacité south east
                SECH = nouvSEH
                SECW = (-nouvNWH + 6 * nouvSEW) // 5
                SEC = (SECH, SECW)
                # remplissage
                if numFils < totalFils:  # il y a (totalFils - 1) capacités
                    remplirZone(image, 1, NWC, SEC, racine.capacites[numFils])
            elif type(racine) is Parallele:  # on divise horizontalement
                # north west
                nouvNWH = NWH + (SEH - NWH) * numFils // totalFils
                nouvNWW = NWW
                # south east
                nouvSEW = SEW
                nouvSEH = NWH + (SEH - NWH) * (numFils + 1) // totalFils
            else:
                raise TypeError("Le type de noeud n'est pas reconnu.")

            nouvNW = (nouvNWH, nouvNWH)
            nouvSE = (nouvSEH, nouvSEW)
            # appel résursif
            creerImage(image, fils, numFils, nouvNW, nouvSE, profondeur + 1)


def moyenneZone(image, canal, NW, SE):
    """
    Donne la moyenne des valeurs d'un condensateur ou d'une résistance sur une
    zone donnée.

    Parameters
    ----------
    image : numpy array
        Image cible.
    canal : int
        Canal cible.
    NW = (NWH, NWH) : (int, int)
        Coin North-West de la portion de l'image.
    SE = (SEH, SEW) : (int, int)
        Coin South-East de la portion de l'image.

    Returns
    -------
    moyenne : float
        Valeur moyenne.
    """
    NWH, NWH = NW
    SEH, SEW = SE
    return np.mean(image[NWH:SEH, NWH:SEW, canal])


# (TBR) "updaterRacine" !
# (TBR) Bien tenté, mais ça ne compte pas comme du français :-D
def modifierRacine(image, racine, numRacine, NW, SE):
    """
    Fonction récursive de mise à jour de la racine de l'arbre.

    Parameters
    ----------
    image : numpy array
        Image à modifier.
    racine : Grille.Noeud
        Noeud que l'on examine.
    numRacine : int
        Numéro de la racine parmi les fils de son père.
    NW = (NWH, NWW) : (int, int)
        Coin North-West de la portion de l'image.
    SE = (SEH, SEW) : (int, int)
        Coin South-East de la portion de l'image.
    """
    NWH, NWH = NW
    SEH, SEW = SE
    # cas de base
    if type(racine) is Feuille:
        racine.val = moyenneZone(image, 0, NW, SE)
        print(f"Feuille de valeur {racine.val}")
    # else...
    else:
        print(f"Noeud")
        for numFils, fils in enumerate(racine.fils):
            totalFils = len(racine.fils)
            if type(racine) is Serie:  # on divise verticalement
                # new north west
                nouvNWH = NWH
                nouvNWW = NWW + (SEW - NWW) * numFils // totalFils
                # new south east
                nouvSEH = SEH
                nouvSEW = NWW + (SEW - NWW) * (numFils + 1) // totalFils
                # Capacity north west
                NWCH = nouvNWH
                NWCW = (nouvNWH + 4 * nouvSEW) // 5
                NWC = (NWCH, NWCW)
                # Capacity south east
                SECH = nouvSEH
                SECW = (-nouvNWH + 6 * nouvSEW) // 5
                SEC = (SECH, SECW)
                if numFils < totalFils:
                    racine.capacites[numFils] = moyenneZone(image, 1, NWC, SEC)
            else:  # on divise horizontalement
                # north west
                nouvNWH = NWH + (SEH - NWH) * numFils // totalFils
                nouvNWW = NWW
                # south east
                nouvSEW = SEW
                nouvSEH = NWH + (SEH - NWH) * (numFils + 1) // totalFils
            nouvNW = (nouvNWH, nouvNWH)
            nouvSE = (nouvSEH, nouvSEW)
            # appel récursif
            modifierRacine(
                racine=racine.fils,
                numRacine=numFils,
                NW=nouvNW,
                SE=nouvSE,
                image=image,
            )
