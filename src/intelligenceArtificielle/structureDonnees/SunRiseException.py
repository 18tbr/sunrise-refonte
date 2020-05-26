"""Définit des exceptions utiles dans les différents fichiers."""


class FeuilleException(Exception):
    """Vous avez utilisé une syntaxe invalide sur une feuille."""

    pass


class NonFeuilleException(Exception):
    """Vous avez utilisé une syntaxe spécifique aux feuilles pour un noeud."""

    pass


class NonMarqueException(Exception):
    """On tente de récupérer le marquage (i.e. la couleur) d'un noeud qui n'a
    pas encore été marqué."""

    pass


class SimulationException(Exception):
    """Une simulation a échoué pour des raisons mathématiques."""

    pass


class ModeleIntrouvable(Exception):
    """Un modèle keras demandé ne peut être trouvé."""

    pass


class ImageTropPetite(Exception):
    """Un arbre est trop gros pour être représenté dans une image demandée."""

    pass


# Une exception levée par l'interface graphique lorsque les différents fichiers de mesure n'ont pas la même base de temps.
class FichierIncoherent(Exception):
    pass


# Une exception levée par l'interface graphique lorsque les différents fichiers de mesure n'ont pas la même base de temps.
class FichierIncoherent(Exception):
    pass
