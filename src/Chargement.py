import matplotlib.pyplot as plt
import matplotlib.animation as anim

figure = plt.figure()
X, Y = [], []
(ligne,) = plt.axes(xlim=(0, 10), ylim=(0, 10)).plot(X, Y)


def initialisationAnimation():
    ligne.set_data(X, Y)
    return (ligne,)


def fonctionAnimation(mot):
    X.append(len(X))
    Y.append(len(mot))
    ligne.set_data(X, Y)
    return (ligne,)


# Coucou
def fonctionGeneratrice():
    # while True:
    for i in range(10):
        yield input("Inscrivez votre Mot:\n---> ")


animationNoyau = anim.FuncAnimation(
    figure,
    fonctionAnimation,
    frames=fonctionGeneratrice,
    init_func=initialisationAnimation,
    blit=True,
)

plt.show()
