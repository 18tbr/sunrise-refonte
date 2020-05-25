"""Ce fichier contient la classe parente abstraite des noeuds qui composent nos
arbres. Presque tous les autres fichiers doivent importer celui ci.

La classe parente contient également de la documentation sur les différentes
méthodes des noeuds des arbres. Notez que la plupart des méthodes sont
implémentées dans les classes filles, d'où les NotImplementedError un peu
partout dans cette classe.
"""


class Noeud(object):
    """Classe pour les noeuds."""

    def __init__(self, arbre=None, parent=None):
        # IMPORTANT : il est presque toujours meilleur d'appeler le constructeur
        # sans argument et de laisser ajoutFils s'occuper de tout.
        super(Noeud, self).__init__()
        self.parent = parent
        self.arbre = None
        self.fils = []
        self._profondeur = None
        # IMPORTANT : il faut toujours attacher en dernier, car attacher peut
        # faire référence à d'autres attributs de la classe.
        if arbre is not None:
            self.attacher(arbre)

    def suppressionFils(self, index):
        """Méthode abstraite, on supprime le fils à l'index i.

        Le noeud est modifié en place, et on renvoie le parent obtenu (car c'est
        plus pratique pour la mutation des arbres).
        """
        raise NotImplementedError(
            "La suppression d'un fils n'a pas été réimplémenté."
        )

    def creationSimulationRecursive(self, A, B, C, gauche, droite, curseur):
        """Méthode abstraite, permet de calculer les matrices qui seront
        utilisées pour le calcul du score de l'arbre proposé."""
        raise NotImplementedError(
            "La création récursive des matrices de simulation n'a pas été implémentée."
        )

    def creationMarquageRecursif(
        self, A, B, C, D, gauche, droite, curseur, conteneur, capaciteDroite
    ):
        """Méthode abstraite, parcourt l'arbre en profondeur et calcule les
        matrices de simulation et la matrice des délais dans notre arbre afin de
        pouvoir faire le calcul de rétropropagation d'erreur."""
        raise NotImplementedError(
            "La création récursive du marquage de l'image n'a pas été réimplémentée."
        )

    def injectionMarquage(self, E, gauche, droite, curseur, capaciteDroite):
        """Méthode abstraite, parcourt l'arbre en notant sur chaque noeud les
        valeurs qui seront utilisées pour l'intensité des trois couleurs de
        l'image."""
        raise NotImplementedError(
            "L'injection récursive du marquage n'a pas été réimplémentée."
        )

    def ajoutFils(self, nouveauFils, index, forme=None):
        """Méthode abstraite, contraire de suppressionFils.

        Le noeud est modifié en place, et on renvoie le parent obtenu (car c'est
        plus pratique pour l'initialisation des arbres).
        """
        raise NotImplementedError("L'ajout d'un fils n'a pas été implémenté.")

    def substituerEnfants(self, listeFils):
        """Méthode abstraite, utile pour la fusion d'arbres. Remplace tous les
        enfants du noeud choisi par ceux passés en argument.

        Dans le cas d'un noeud série, on conserve autant de capacités que
        possible.
        """
        raise NotImplementedError(
            "La subtitution de noeuds enfants n'a pas été réimplémentée."
        )

    @property
    def profondeur(self):
        """Implémentation abstraite de la profondeur."""
        raise NotImplementedError(
            "Le calcul de la profondeur d'un noeud n'a pas été implémenté."
        )

    def remplacer(self, nouveau):
        """Remplace l'instance noeud désignée par nouveau dans son parent.

        Il s'agit d'une méthode interne à la classe noeud qui ne doit pas être
        appelée de l'extérieur.
        """
        if self.parent is not None:
            # On trouve l'indice de l'élément actuel dans la liste fils du
            # parent
            indexParent = self.parent.fils.index(self)
            self.parent.fils[indexParent] = nouveau
        elif self.arbre is not None:
            # Autre cas important à traiter : on est en train de changer la
            # racine de l'arbre
            self.arbre.racine = nouveau
        else:
            raise IndexError(
                "L'indivdu selectionné n'a pas de parent et n'est pas la racine d'un arbre, il n'y a donc nulle part où le remplacer."
            )
        nouveau.parent = self.parent
        # On attache le nouvel élément à la arbre
        nouveau.attacher(self.arbre)
        # Dans la mesure où l'on a perdu notre place dans l'arbre, il faut s'en
        # détacher.
        self.detacher()

    def sousArbre(self):
        """Méthode abstraite, utile pour la fusion d'arbres. Renvoie une copie
        de tout le sousArbre qui se trouve au dela de cet arbre, mais sans
        parent pour ce noeud et sans arbre associé.
        """
        raise NotImplementedError(
            "La création d'un sous-arbre à partir d'un noeud n'a pas été implémentée."
        )

    def attacher(self, arbre):
        """Méthode abstraite, attache un noeud et tous ses fils récursivement à
        un arbre, en mettant au passage à jour les caractéristiques de la
        arbre.

        Doit être appelé après avoir donné un parent au noeud considéré. Cette
        étape est utile pour garder des arbres cohérents après les étapes de
        fusion.
        """
        raise NotImplementedError(
            "L'attachement d'un noeud à un arbre n'a pas été implémentée."
        )

    def detacher(self, perdreParent=True):
        """Méthode abstraite, pendant de `attacher` utilisé pour la suppression.

        L'attribut perdre parent a été ajouté suite à des bugs ; en fait, si
        l'on détache tout un sous arbre on veut que seul le sommet le sommet du
        sous arbre perde le référence à son parent, mais l'intérieur de l'arbre
        doit rester cohérent. De l'extérieur, il n'y a normalement jamais besoin
        d'appeler `detacher` du tout, mais s'il le faut il est sans doute plus
        judicieux de ne pas passer d'argument.
        """
        raise NotImplementedError(
            "Le détachement d'un noeud d'un arbre n'a pas été implémenté."
        )

    def dessiner(self, image, coinHautGauche, coinBasDroite):
        """Méthode abstraite, à utiliser récursivement pour obtenir la
        représentation sous forme d'image de l'arbre."""
        raise NotImplementedError(
            "La coloration de l'image à partir d'un noeud n'a pas été réimplémenté."
        )

    def lire(self, image, coinHautGauche, coinBasDroite, conteneur):
        """Méthode abstraite, à utiliser récursivement pour mettre à jour un
        arbre à partir d'une image.

        Renvoie la valeur de la capacité à droite du noeud donné. On utilise le
        même système de conteneur que dans `creationMarquageRecursif` pour
        éviter les problèmes de non linéarité dans les calculs avec les liaisons
        parallèles.
        """
        raise NotImplementedError(
            "La mise à jour d'un arbre à partir d'une image n'a pas été réimplémenté."
        )

    def normaliser(self, image, coinHautGauche, coinBasDroite):
        """Méthode abstraite, à utiliser récursivement pour normaliser une image
        en lui donnant la forme de l'arbre souhaité."""
        raise NotImplementedError(
            "La normalisation d'une image à partir d'un arbre n'a pas été réimplémenté."
        )

    def elaguerSousArbre(self, coinHautGauche, coinBasDroite):
        """Méthode abstraite, à utiliser récursivement sur un arbre pour
        l'élaguer."""
        raise NotImplementedError(
            "L'élaguage d'un sous arbre n'a pas été réimplémenté."
        )


def conversionIndice(indice):
    """Convertit l'indice utile pour A, B et C en un indice utile pour D,
    important car Text ne se trouve pas dans A alors qu'il est dans D.

    Utile dans `Serie.creationMarquageRecursif` et `Feuille.injectionMarquage`.
    """
    if indice is None:
        return 0
    else:
        return indice + 1
