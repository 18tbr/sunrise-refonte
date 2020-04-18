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

Si dans le fichier `Groupe.py` vous avez :
```py
class Multiplie(object):
    def __init__(self):
        super(double, self).__init__()

    def multipliePar2(self, x):
        return 2 * x
```

Alors dans le fichier `test_Groupe.py` on pourra écrire :
```py
def test_multiplieFonction():
    """Teste si multipliePar2(3) = 6"""
    multiplie = Multiplie()
    assert multiplie.multipliePar2(3) == 6
```

## Lancer les tests

Pour lancer tous les tests du dossier `tests` :
```bash
>> pytest
```

Pour lancer les tests du fichier `test_Groupe.py` :
```bash
>> pytest tests\test_Groupe.py
```

