# Poetry

Poetry est l'outil utilisé pour __créer et publier le package pip du projet__. Dans ce document, on présente l'usage général de poetry afin de permettre de maintenir la package sur le long terme.

## Pouquoi un package ?

Le fait de créer un package permet de __distribuer l'outil très facilement__ à des tiers en s'assurant que toutes les dépendances du projet sont bien spécifiées.

Pour qu'un tiers puisse utiliser l'outil __sunrise__ créé pour ce projet, il lui suffit de l'installer avec pip et tout fonctionne diectement (moyennant des bugs dans le projet) :

```sh
pip install sunriseces
```

## Package Python

Les package python que l'on peut télécharger avec pip sont stocké sur [PyPi](https://pypi.org) ("PYthon Package Index"). Pour pouvoir publier un package sur PyPi il faut __disposer d'un compte sur le site__. Actuellement, le package pip du projet (nommé "sunriseces") se trouve sur mon compte pypi (roadelou).

Notez que pour apprendre à utiliser PyPi et à publier ses packages, le site fourni aussi un mirroir de test nommé [TestPyPi](https://test.pypi.org). Il est recommandé de __tester les différents outils sur TestPyPi__ avant de faire une publication sur le vrai PyPi.

## Poetry

[Poetry](https://python-poetry.org) est un outil permettant de créer des packages python assez facilement. Il existe également d'autres outils pour réaliser cette tache, on mentionnera notamment setuptools et flint. La raison pour laquelle nous avons choisi d'utiliser poetry est que l'outil est __assez simple__ et qu'il permet de __gérer complètement les dépendances de versions__.

Poetry repose essentiellement sur deux fichiers :
 - pyproject.toml
 - poetry.lock

L'outil poetry est utilisé en ligne de commande, tout son fonctionnement est décrit sur [le site du projet](https://python-poetry.org/docs/).

:warning: Attention, poetry va tenter de trouver lui même la version de python à utiliser avec votre projet en utilisant le nom _python_. Or sous la plupart des distributions Linux, _python_ fait en fait référence à python2 et non python3. Une façon d'aider poetry à utiliser la bonne version de python est de le lancer avec python3 vous même :

```sh
python3 ~/.poetry/bin/poetry $ARGUMENTS
```

Pour éviter de faire cela vous-même à chaque fois, sous bash vous pouvez __créer une fonction qui le fasse automatiquement__ (les alias bash sont considérés _obsolètes_). Pour ce faire, il vous suffit d'ajouter dans votre fichier ~/.bash\_aliases (ou ailleurs suivant votre organisation):

```sh
function poetry {
  # Le '$@' désigne tous les arguments que l'on a passé en appelant poetry.
  python3 ~/.poetry/bin/poetry $@
}
```

Cette méthode peut sans doute être adaptée à d'autre shell (si vous n'utilisez pas bash).

Sous Windows, _python_ correspond par défaut à python3, donc vous ne devriez pas rencontrer de problèmes.

## pyproject.toml

Le fichier pyproject.toml est un fichier de configuration qui __indique à poetry comment construire votre package__. Il peut être mis à jour en utilisant poetry en utilisant des commandes telles que :

```sh
# Ajouter une dépendance à poetry
poetry add $dependance

# Ajouter une dépendance pour les developpeurs du projet SunRise
poetry add -D $dependance

# Changer la version du package
poetry version $version
```

Vous pouvez (et devez) aussi __modifier le pyproject.toml vous même__, il s'agit d'un fichier texte que vous pouvez ouvrir avec l'éditeur de votre choix. Editer le pyproject.toml est particluièrement utile pour __spécifier les points d'entrée du code__, c'est à dire ce que doit lancer python lorsque l'on utilise le package sunriseces en ligne de commande.

En dehors de cela, deux commandes interactives dont vous ne devriez pas avoir besoin pour ce projet sont :

```sh
# Créer un nouveau projet python avec un nouveau fichier pyproject.toml
poetry new $projet

# Créer un nouveau fichier pyproject.toml dans un projet existant
poetry init
```

## poetry.lock

Une des forces de poetry est la gestion des dépendances. Poetry est capable de résoudre toutes les versions possibles des packages que vous avez spécifiés en dépendances. La principale utilité de cela est de s'assurer que si les dépendaces de sunrise font des montées en version qui cassent des fonctions ou interfaces que le projet sunrise utilise, il sera __toujours possible d'installer sunriseces__ car les packages installés en dépendance seront les anciennes version qui fonctionnent.

Toutes ces information sur __les versions calculées des dépendances sont stockées dans le fichier poetry.lock__. Il s'agit d'un fichier de texte mais qui n'est pas vraiment lisible par un humain.

Pour créer le fichier poetry.lock, la commande à utiliser est :

```sh
# La commande de base
poetry lock

# Si jamais poetry est très long à réaliser cette commande, n'hésitez pas à demander des informations de debug avec :
poetry lock -vvv
```

:warning: En pratique cette commande peut être __très longue__ parce que poetry a besoin de télécharger certains packages intégralement afin de lire leur fichier setup.py . Pour des packages comme numpy ou matplotlib, cela peut prendre de longues minutes.

Une fois le fichier poetry.lock créé, vous pouvez __construire le package pip__ à l'aide de la commande :

```sh
poetry build
```

Cette commande devrait créer une __archive du code distribué__ (fichier .tar.gz) et le __package wheel utilisé par pip__ (fichier .whl) correspondant dans un dossier dist. Vous pouvez inspecter votre package avant de le distribuer en décompressant l'archive tar. Sous Linux, la commande correspondante est :

```sh
# Le x signifie "décompresser", le v "afficher des informations", et le fz correspondent il me semble au format .tar.gz
tar -xvzf $archive
```

Enfin, pour publier le package sur pypi, vous pouvez utiliser la commande interactive :

```sh
# Pour publier sur PyPi
poetry publish

# Pour publier vers un autre index qui a déjà été configuré (cf la doc de poetry)
poetry publish -r $index
```
