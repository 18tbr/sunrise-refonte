# Tests

## Structure dans le dossier

Pour chaque groupe `Groupe`, il y a un fichier `Groupe.py`, qui contient le code principal, et un fichier `test_Groupe.py`, qui contient les tests des fonctions :

```bash
sunrise-refonte
|__ src
|   |__ Groupe.py
|   |__ ...
|__ tests
|   |__ test_Groupe.py
|   |__ ...
|__ ci.py
```

## Un exemple de test

Si le fichier `Groupe.py` est :
```py
class Multiplie(object):
    def __init__(self):
        super(double, self).__init__()

    def multipliePar2(self, x):
        return 2 * x
```

Alors le fichier `test_Groupe.py` contient :
```py
def test_multiplieFonction():
    """Teste si multipliePar2(3) = 6"""
    multiplie = Multiplie()
    assert multiplie.multipliePar2(3) == 6
```

## Lancer les tests

Pour lancer les tests, utiliser la fonctionnalité `test` du `ci.py`.
