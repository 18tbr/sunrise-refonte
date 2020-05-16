import numpy as np
from Noeuds import Noeud, Feuille, Parallele, Serie
import matplotlib.pyplot as plt # Utile pour le debuggage uniquement, à supprimer après.

def remplirZone(image, canal, coinHautGauche, coinBasDroite, val):
    """
    Colorie une zone de l'image.

    Parameters
    ----------
    image : numpy array
        Image à remplir.
            canal : int
        Canal cible.
            coinHautGauche = (coinHautGaucheY, coinHautGaucheX) : (int, int)
        Coin North-West de la portion de l'image.
    coinBasDroite = (coinBasDroiteY, coinBasDroiteX) : (int, int)
        Coin South-East de la portion de l'image.
    val : int
        Valeur avec laquelle colorier la portion d'image.

    Returns
    -------
    La fonction modifie `image` en place.
    """
    print(f"On colorie le canal {canal} de {coinHautGauche} à {coinBasDroite}")
    coinHautGaucheY, coinHautGaucheX = coinHautGauche
    coinBasDroiteY, coinBasDroiteX = coinBasDroite
    image[
        coinHautGaucheY:coinBasDroiteY, coinHautGaucheX:coinBasDroiteX, canal
    ] = val


def creerImage(
    image, racine, numRacine, coinHautGauche, coinBasDroite, profondeur
):
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
    coinHautGauche = (coinHautGaucheY, coinHautGaucheX) : (int, int)
        Coin North-West de la portion de l'image.
    coinBasDroite = (coinBasDroiteY, coinBasDroiteX) : (int, int)
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
    # Debug
    afficherImageDebug(image)
    # Récupération des coordonnées
    coinHautGaucheY, coinHautGaucheX = coinHautGauche
    coinBasDroiteY, coinBasDroiteX = coinBasDroite
    # cas de base
    if type(racine) is Feuille:
        print(f"Feuille de valeur {racine.H}")
        remplirZone(image, 0, coinHautGauche, coinBasDroite, racine.H)
        remplirZone(image, 2, coinHautGauche, coinBasDroite, profondeur)
    # else...
    else:
        print(f"Noeud")
        for numFils, fils in enumerate(racine.fils):
            totalFils = len(
                racine.fils
            )  # (TBR) Vous pouvez le calculer une fois hors de la boucle
            if type(racine) is Serie:  # on divise verticalement
                # (TBR) Non, vous savez déjà si racine est de type Serie avant de rentrer dans votre boucle for.
                # new north west
                nouvCoinHautGaucheY = coinHautGaucheY
                nouvCoinHautGaucheX = (
                    coinHautGaucheX
                    + (coinBasDroiteX - coinHautGaucheX) * numFils // totalFils
                )
                # new south east
                nouvCoinBasDroiteY = coinBasDroiteY
                nouvCoinBasDroiteX = (
                    coinHautGaucheX
                    + (coinBasDroiteX - coinHautGaucheX)
                    * (numFils + 1)
                    // totalFils
                )
                # capacité north west
                coinHautGaucheCapaciteY = nouvCoinHautGaucheY
                coinHautGaucheCapaciteX = (
                    nouvCoinHautGaucheX + 4 * nouvCoinBasDroiteX
                ) // 5
                coinHautGaucheCapacite = (
                    coinHautGaucheCapaciteY,
                    coinHautGaucheCapaciteX,
                )
                # capacité south east
                coinBasDroiteCapaciteY = nouvCoinBasDroiteY
                coinBasDroiteCapaciteX = (
                    -nouvCoinHautGaucheX + 6 * nouvCoinBasDroiteX
                ) // 5
                coinBasDroiteCapacite = (
                    coinBasDroiteCapaciteY,
                    coinBasDroiteCapaciteX,
                )
                # remplissage
                if numFils + 1 < totalFils:  # il y a (totalFils - 1)
                    remplirZone(
                        image,
                        1,
                        coinHautGaucheCapacite,
                        coinBasDroiteCapacite,
                        racine.capacites[numFils],
                    )
            elif type(racine) is Parallele:  # on divise horizontalement
                # north west
                nouvCoinHautGaucheY = (
                    coinHautGaucheY
                    + (coinBasDroiteY - coinHautGaucheY) * numFils // totalFils
                )
                nouvCoinHautGaucheX = coinHautGaucheX
                # south east
                nouvCoinBasDroiteX = coinBasDroiteX
                nouvCoinBasDroiteY = (
                    coinHautGaucheY
                    + (coinBasDroiteY - coinHautGaucheY)
                    * (numFils + 1)
                    // totalFils
                )
            else:
                raise TypeError("Le type de noeud n'est pas reconnu.")

            nouvHautGauche = (nouvCoinHautGaucheY, nouvCoinHautGaucheY)
            nouvBasDroite = (nouvCoinBasDroiteY, nouvCoinBasDroiteX)
            # appel récursif
            creerImage(
                image,
                fils,
                numFils,
                nouvHautGauche,
                nouvBasDroite,
                profondeur + 1,
            )


def moyenneZone(image, canal, coinHautGauche, coinBasDroite):
    """
    Donne la moyenne des valeurs d'un condensateur ou d'une résistance sur une
    zone donnée.

    Parameters
    ----------
    image : numpy array
        Image cible.
    canal : int
        Canal cible.
    coinHautGauche = (coinHautGaucheY, coinHautGaucheX) : (int, int)
        Coin North-West de la portion de l'image.
    coinBasDroite = (coinBasDroiteY, coinBasDroiteX) : (int, int)
        Coin South-East de la portion de l'image.

    Returns
    -------
    moyenne : float
        Valeur moyenne.
    """
    coinHautGaucheY, coinHautGaucheX = coinHautGauche
    coinBasDroiteY, coinBasDroiteX = coinBasDroite
    return np.mean(
        image[
            coinHautGaucheY:coinBasDroiteY,
            coinHautGaucheX:coinBasDroiteX,
            canal,
        ]
    )


# (TBR) "updaterRacine" !
# (TBR) Bien tenté, mais ça ne compte pas comme du français :-D
def modifierRacine(image, racine, numRacine, coinHautGauche, coinBasDroite):
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
    coinHautGauche = (coinHautGaucheY, coinHautGaucheX) : (int, int)
        Coin North-West de la portion de l'image.
    coinBasDroite = (coinBasDroiteY, coinBasDroiteX) : (int, int)
        Coin South-East de la portion de l'image.
    """
    coinHautGaucheY, coinHautGaucheX = coinHautGauche
    coinBasDroiteY, coinBasDroiteX = coinBasDroite
    # cas de base
    if type(racine) is Feuille:
        racine.H = moyenneZone(image, 0, coinHautGauche, coinBasDroite)
        print(f"Feuille de valeur {racine.H}")
    # else...
    else:
        print(f"Noeud")
        for numFils, fils in enumerate(racine.fils):
            totalFils = len(racine.fils)
            if type(racine) is Serie:  # on divise verticalement
                # new north west
                nouvCoinHautGaucheY = coinHautGaucheY
                nouvCoinHautGaucheX = (
                    coinHautGaucheX
                    + (coinBasDroiteX - coinHautGaucheX) * numFils // totalFils
                )
                # new south east
                nouvCoinBasDroiteY = coinBasDroiteY
                nouvCoinBasDroiteX = (
                    coinHautGaucheX
                    + (coinBasDroiteX - coinHautGaucheX)
                    * (numFils + 1)
                    // totalFils
                )
                # Capacity north west
                coinHautGaucheCapaciteY = nouvCoinHautGaucheY
                coinHautGaucheCapaciteX = (
                    nouvCoinHautGaucheY + 4 * nouvCoinBasDroiteX
                ) // 5
                coinHautGaucheCapacite = (
                    coinHautGaucheCapaciteY,
                    coinHautGaucheCapaciteX,
                )
                # Capacity south east
                coinBasDroiteCapaciteY = nouvCoinBasDroiteY
                coinBasDroiteCapaciteX = (
                    -nouvCoinHautGaucheY + 6 * nouvCoinBasDroiteX
                ) // 5
                coinBasDroiteCapacite = (
                    coinBasDroiteCapaciteY,
                    coinBasDroiteCapaciteX,
                )
                if numFils < totalFils:
                    racine.capacites[numFils] = moyenneZone(
                        image, 1, coinHautGaucheCapacite, coinBasDroiteCapacite
                    )
            else:  # on divise horizontalement
                # north west
                nouvCoinHautGaucheY = (
                    coinHautGaucheY
                    + (coinBasDroiteY - coinHautGaucheY) * numFils // totalFils
                )
                nouvCoinHautGaucheX = coinHautGaucheX
                # south east
                nouvCoinBasDroiteX = coinBasDroiteX
                nouvCoinBasDroiteY = (
                    coinHautGaucheY
                    + (coinBasDroiteY - coinHautGaucheY)
                    * (numFils + 1)
                    // totalFils
                )
            nouvHautGauche = (nouvCoinHautGaucheY, nouvCoinHautGaucheY)
            nouvBasDroite = (nouvCoinBasDroiteY, nouvCoinBasDroiteX)
            # appel récursif
            modifierRacine(
                racine=racine.fils,
                numRacine=numFils,
                coinHautGauche=nouvHautGauche,
                coinBasDroite=nouvBasDroite,
                image=image,
            )

# Une fonction de Debug, à supprimer plus tard
def afficherImageDebug(image):
    R, V, B = image[:,:,0], image[:,:,1], image[:,:,2]
    plt.imshow(image)
    plt.colorbar()
    plt.show()

    plt.imshow(R, cmap='jet')
    plt.colorbar()
    plt.show()

    plt.imshow(V, cmap='jet')
    plt.colorbar()
    plt.show()

    plt.imshow(B, cmap='jet')
    plt.colorbar()
    plt.show()
