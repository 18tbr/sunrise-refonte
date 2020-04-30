import sklearn
import joblib

class Genetique(object):
    """docstring for Genetique."""

    def __init__(self, args, parametres, sorties, experience):
        super(Genetique, self).__init__()
        # Les arguments de l'experience
        self.args = args
