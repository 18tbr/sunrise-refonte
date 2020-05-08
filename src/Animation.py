import matplotlib.pyplot as plt


class Animation(object):
    """docstring for Animation."""

    def __init__(self, args, sorties):
        super(Animation, self).__init__()
        # Les arguments de la simulation, récupérés du groupe SunRise
        self.args = args
        # Les sorties de la simulation, ce que l'on cherche à animer
        self.sorties = sorties
        # Le résultat de l'animation, ce que le groupe UI voudra afficher.
        self.animation = None
