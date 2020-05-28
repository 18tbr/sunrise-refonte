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


## Fichiers de script

Dans la mesure où nous étions __contraints par le temps__ pour cette année, nous n'avons __pas écrit des tests pour tous les modules__ et nous sommes parfois contentés de vérifier qu'ils marchaient sur des __script simples__. Pour différentier ces scripts des tests, nous avons fait commmencer leur nom par `script\_`.

__Ces scripts ne se substituent pas aux tests__, il faudra à terme écrire des tests pour ce qui manque. Nous avons tout de même laissé ces script dans le dépôt pour __aider à comprendre un peu comment le code est censé être utilisé__.

Notez que tous ces scripts sont censés être lancés depuis la racine du dépôt, c'est à dire avec une commande comme :

```sh
# Sous Linux
python3 tests/script\_$nom

# De même sous Windows
python tests/script\_$nom 
```
