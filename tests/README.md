# Tests

## Un exemple de test

Si le fichier `foo.py` est :
```py
class Multiplie(object):
    def __init__(self):
        super(double, self).__init__()

    def multipliePar2(self, x):
        return 2 * x
```

Alors le fichier `test_foo.py` contient :
```py
def test_multiplieFonction():
    """Teste si multipliePar2(3) = 6"""
    multiplie = Multiplie()
    assert multiplie.multipliePar2(3) == 6
```

## Lancer les tests

Pour lancer les tests, utiliser la fonctionnalité `test` de `ci.py`.


## Fichiers de script

Dans la mesure où nous étions __contraints par le temps__ pour cette année, nous n'avons __pas écrit de tests pour tous les modules__ et nous nous sommes parfois contentés de vérifier qu'ils marchaient sur des __scripts simples__. Pour différencier ces scripts des tests, nous avons fait commmencer leur nom par `script_`.

__Ces scripts ne se substituent pas aux tests__, il faudra à terme écrire des tests pour ce qui manque. Nous avons tout de même laissé ces scripts dans le dépôt pour __aider à comprendre un peu comment le code est censé être utilisé__.

Notez que tous ces scripts sont censés être lancés depuis la racine du dépôt, c'est à dire avec une commande comme :
```sh
# Sous Linux
python3 tests/script_$nom

# De même sous Windows
python tests/script_$nom 
```
