import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
plt.style.use('ggplot')

class Animation(object):
    """docstring for Animation."""

    def __init__(self, args,size,tmin,tmax, sorties):
        super(Animation, self).__init__()
        # Les arguments de la simulation, récupérés du groupe SunRise
        self.args = args
        #taille de la fenêtre
        self.size=size
        self.tmin=tmin
        self.tmax=tmax
        # Les sorties de la simulation, ce que l'on cherche à animer
        #une matrice np dont les lignes sont les courbes à afficher
        self.sorties = sorties
        # Le résultat de l'animation, ce que le groupe UI voudra afficher.
        self.animation = None

    
    def animer(self):

        fig, ax = plt.subplots(figsize=self.size)
        ax.set(xlim=(self.tmin, self.tmax), ylim=(np.min(self.sorties), np.max(self.sorties)))
        (a,b)=np.shape(self.sorties)
        
        t = np.linspace(self.tmin, self.tmax, b)    
        
        line = ax.plot(t, self.sorties[0, :], color='k', lw=2)[0]
        
        def animate(i):
            line.set_ydata(self.sorties[i, :])
            
        anim = FuncAnimation(
            fig, animate, interval=100, frames=a-1, repeat=False)
         
        plt.draw()
        plt.show()