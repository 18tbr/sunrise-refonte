# Un fichier pour définir des exceptions utiles dans les différents fichiers.


class FeuilleException(Exception):
    """Une erreur est apparue car vous utilisé une syntaxe invalide sur une
    feuille."""
    pass


class NonFeuilleException(Exception):
    """Une erreur est apparue car vous avez utilisé une syntaxe spécifique aux
    feuilles pour un noeud."""
    pass


class NonMarqueException(Exception):
    """Une erreur qui signale que l'on tente de récupérer le marquage (i.e. la
    couleur) d'un noeud qui n'a pas encore été marqué."""
    pass

# Une exception utile pour signifier qu'une simulation a échoué pour des raisons mathématiques.
class SimulationException(Exception):
    pass
