# Ce fichier contient la classe parente abstraite des neouds qui composent nos arbres. Presque tous les autres fichiers doivent importer celui ci. La classe parente contient également de la documentation sur les différentes méthodes des noeuds des arbres. Notez que la plupart des méthodes sont implémentées dans les classes filles, d'où les NotImplementedError un peu partout dans cette classe.


class Noeud(object):
    """docstring for Noeud."""

    def __init__(self, grille=None, parent=None):
        # IMPORTANT : il est presque toujours meilleur d'appeller le constructeur sans argument et de laisser ajoutFils s'occuper de tout.
        super(Noeud, self).__init__()
        self.parent = parent
        self.grille = None
        self.fils = []
        self._profondeur = None
        # IMPORTANT : il faut toujours attacher en dernier, car attacher peut faire référence à d'autres attributs de la classe.
        if grille is not None:
            self.attacher(grille)

    # Méthode abstraite, on supprime le fils à l'index i
    # Le noeud est modifié en place, et on renvoie le parent obtenu (car c'est plus pratique pour la mutation des arbres).
    def suppressionFils(self, index):
        raise NotImplementedError(
            "La suppression d'un fils n'a pas été réimplémenté."
        )

    # Méthode qui permet de calculer les matrices qui seront utilisées pour le calcul du score de l'arbre proposé.
    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
        raise NotImplementedError(
            "La création récursive des matrices de simulation n'a pas été implémentée."
        )

    # La Méthode abstraite qui parcourt l'arbre en profondeur qui calcule les matrices de simulation et la matrice des délais dans notre arbre afin de pouvoir faire le calcul de rétro propagation d'erreur..
    def creationMarquageRecursif(
        self, A, B, C, D, gauche, droite, curseur, conteneur, capaciteDroite
    ):
        raise NotImplementedError(
            "La création récursive du marquage de l'image n'a pas été réimplémentée."
        )

    # Méthode qui permet de parcourir l'arbre en notant sur chaque noeud les valeurs qui seront utilisées pour l'intensité des trois couleurs de l'image.
    def injectionMarquage(self, E, gauche, droite, curseur, capaciteDroite):
        raise NotImplementedError(
            "L'injection récursive du marquage n'a pas été réimplémentée."
        )

    # Méthode abstraite, contraire de suppressionFils
    # Le noeud est modifié en place, et on renvoie le parent obtenu (car c'est plus pratique pour l'initialisation des arbres)
    def ajoutFils(self, nouveauFils, index, forme=None):
        raise NotImplementedError("L'ajout d'un fils n'a pas été implémenté.")

    # Méthode utile pour la fusion d'arbres, elle sert à remplacer tous les enfants du noeud choisi par ceux passés en argument. Dans le cas d'un noeud série, on conserve autant de capacités que possible.
    def substituerEnfants(self, listeFils):
        raise NotImplementedError(
            "La subtitution de noeuds enfants n'a pas été réimplémentée."
        )

    # Implémentation abstraite de la profondeur
    @property
    def profondeur(self):
        raise NotImplementedError(
            "Le calcul de la profondeur d'un noeud n'a pas été implémenté."
        )

    # Une fonction pour remplacer l'instance noeud désignée par nouveau dans son parent. Il s'agit d'une méthode interne à la classe noeud qui ne doit pas être appelée de l'extérieur.
    def remplacer(self, nouveau):
        if self.parent is not None:
            # On trouve l'indice de l'élément actuel dans la liste fils du parent
            indexParent = self.parent.fils.index(self)
            self.parent.fils[indexParent] = nouveau
        elif self.grille is not None:
            # Autre cas important à traiter : on est en train de changer la racine de l'arbre
            self.grille.racine = nouveau
        else:
            raise IndexError(
                "L'indivdu selectionné n'a pas de parent et n'est pas la racine d'un arbre, il n'y a donc nulle part où le remplacer."
            )
        nouveau.parent = self.parent
        # On attache le nouvel élément à la grille
        nouveau.attacher(self.grille)
        # Dans la mesure où l'on a perdu notre place dans l'arbre, il faut s'en détacher.
        self.detacher()

    # Renvoie une copie de tout le sousArbre qui se trouve au dela de cette grille, mais sans parent pour ce noeud et sans grille associée.
    # Cette méthode est utile pour faire des fusions d'arbres.
    def sousArbre(self):
        raise NotImplementedError(
            "La création d'un sous-arbre à partir d'un noeud n'a pas été implémentée."
        )

    # Attache un noeud et tous ses fils récursivement à une grille, en mettant au passage à jour les caractéristiques de la grille. Doit être appelé après avoir donné un parent au noeud considéré. Cette étape est utile pour garder des grilles cohérentes après les étapes de fusion.
    def attacher(self, grille):
        raise NotImplementedError(
            "L'attachement d'un noeud à une grille n'a pas été implémentée."
        )

    # Pendant de attacher utilisé pour la suppression. L'attribut perdre parent a été ajouté suite à des bugs, enfait si on détache tout un sous arbre on veut que seul le sommet le sommet du sous arbre perde le référence à son parent, mais l'intérieur de l'arbre doit rester cohérent. De l'extérieur, il n'y a normalement jamais besoin d'appeler detacher du tout, mais s'il le faut il est sans doute plus judicieux de ne pas passer d'argument.
    def detacher(self, perdreParent=True):
        raise NotImplementedError(
            "Le détachement d'un noeud d'une grille n'a pas été implémenté."
        )

    # Méthode à appeller récursivement pour obtenir la représentation sous forme d'image de l'arbre.
    def dessiner(self, image, coinHautGauche, coinBasDroite):
        raise NotImplementedError(
            "La coloration de l'image à partir d'un noeud n'a pas été réimplémenté."
        )

    # Méthode à utiliser récursivement pour mettre à jour un arbre à partir d'une image. Renvoie la valeur de la capacité à droite du noeud donné. On utilise le même système de conteneur que dans creationMarquageRecursif pour éviter les problèmes de non linéarité dans les calculs avec les liaisons parallèles.
    def lire(self, image, coinHautGauche, coinBasDroite, conteneur):
        raise NotImplementedError(
            "La mise à jour d'un arbre à partir d'une image n'a pas été réimplémenté."
        )

    # Méthode à utiliser récursivement pour normaliser une image en lui donnant la forme de l'arbre souhaité
    def normaliser(self, image, coinHautGauche, coinBasDroite):
        raise NotImplementedError(
            "La normalisation d'une image à partir d'un arbre n'a pas été réimplémenté."
        )


# Une fonction pour convertir l'indice utile pour A, B et C en un indice utile pour D, important car Text ne se trouve pas dans A alors qu'il est dans D. Utile dans Serie.creationMarquageRecursif et Feuille.injectionMarquage
def conversionIndice(indice):
    if indice is None:
        return 0
    else:
        return indice + 1
