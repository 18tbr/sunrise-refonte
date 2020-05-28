# DevOps

Ce fichier est un petit guide de la gestion de ce dépôt destiné au __groupe DevOps__ du projet SunRise.

Le rôle du groupe DevOps est de __mettre à disposition des contributeurs du projet (et en particulier les membres du projet SunRise) les ressources dont ils ont besoin__ pour pouvoir se concentrer sur le code à écrire. Cela contient en particulier le fait de gérer l'__intégration continue__ de ce dépôt.

## Organisation de sunrise-refonte

Le flux de travail proposé pour ce dépôt est assez simple _en théorie_.
1. Les membres du projet ont __chacun une branche personnelle__ pour pouvoir __déposer :outbox_tray: leur code après une séance de travail__.
2. Entre deux séances de travail :watch:, le groupe DevOps se charge de réaliser la __fusion des codes__ écrits sur la branche `devops` du dépôt.
3. Enfin, une fois la fusion réalisée, il ne reste qu'à __remettre à jour__ :inbox_tray: la branche `master` du dépôt et les branches de tous les membres afin qu'ils puissent travailler normalement à la séance suivante.

Le principal avantage de cette approche est que __les membres du projet ne rencontrent normalement jamais de conflits__ lorsqu'ils synchronisent leur branche par rapport à master ou lorsqu'ils poussent leur modifications sur GitHub. On peut ainsi __travailler plus facilement avec des membres qui ne connaissent pas du tout git__ :+1: sans perdre de temps à le leur expliquer.

Le gros défaut de cette approche est que __la fusion des différentes branches entre les séances de travail est souvent très laborieuse__ :-1: Si l'usage de dépôt ne nécessite aucune connaissance de git pour les contributeurs, sa gestion par les membres du groupe DevOps en requiert au contraire une compréhension assez fine :expressionless:

## `ci.py` pour le groupe DevOps

Le script `ci.py` comporte, en plus des fonctions documentées dans l'interface, un certain nombre de __fonctions destinées à l'usage du groupe DevOps__ :toolbox: _Il y a d'ailleurs plus de fonctions cachées que de fonctions publiques dans ce script_. Ces fonction cachées sont :
- fusion
- union
- test
- format

### Fusion

La fonction fusion du script `ci.py` sert _en théorie_ à __fusionner automatiquement__ les branches des contributeurs dans `devops`. En pratique, __des conflits arrivent très souvent__, et il faut la plupart du temps les résoudre à la main :writing_hand: avec git.

:warning: La fonction fusion est écrite de telle sorte que __les branches des contributeurs ne sont pas modifiées__. Cela permet de revenir en arrière facilement si l'on constate une perte de leur travail. Surtout, ne modifiez pas les branches des contributeurs pendant l'étape de fusion :bangbang:

Pour __vérifier si une partie du travail des contributeurs a été perdue__ lors d'une fusion, une façon simple est d'utiliser :
```bash
git log --oneline
```

Si un problème survient lors d'une fusion sur la branche `devops`, il faudra sans doute __revenir en arrière :leftwards_arrow_with_hook: et essayer une approche différente__. Pour cela, vous pouvez utiliser :
```bash
git reset --hard $COMMIT
```

La fusion est également un bon moment pour _formater le code, corriger les erreurs de nommage et faire des revues de code en général_ :heavy_check_mark:

### Union

Une fois que toutes les fusions ont été réalisées, il faut __mettre à jour la branche `master` et toutes les branches des contributeurs__. Si la fusion a été gérée correctement, l'__union ne devrait pas poser de problèmes__ :smiley:, sinon vous pouvez à cette étape aussi avoir des conflits à régler avec git.

:warning: Une fois la fusion réalisée, il devient __beaucoup plus difficile de revenir en arrière__ :facepalm: pour corriger une erreur éventuelle dans la fusion. __Vérifiez bien que votre fusion est correcte avant de faire l'union__ :bangbang:

### Test

La fonction test permet de __lancer tous les tests du code__ écrits dans le dossier `test`. Cette fonction est celle __utilisée par GitHub__ pour vérifier la validité du build :crossed_fingers: Vous pouvez aussi l'utiliser en local si vous avez le module `pytest` installé.

Pour installer rapidement tous les modules nécessaires aux tests des codes dans le dépôt, vous pouvez utiliser le `requirements.txt` présent dans le dossier `devops`.

### Format

La fonction format sert à __formater le code__ (:thinking:). Elle a été concue pour fonctionner avec `black`, que vous pouvez également installer avec le `requirements.txt` présent dans le dossier `devops`.

La commande pour utiliser `black` sur un fichier comme le ferait `ci.py` est :
```bash
python3 -m black -l 80 $FICHIER
```

## flake8

[flake8](https://github.com/pycqa/flake8) est un outil qui permet de __detecter certaines erreurs de codes__ (erreurs de syntaxe, variables non déclarées) sans lancer le code. C'est une des __étapes de vérification programmées sur GitHub__. La syntaxe pour lancer la vérification sur votre machine comme le ferait GitHub est _(en se plaçant dans le dossier de ci.py)_ :

```sh
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Conclusion

Avec toutes ces informations, vous devriez être __prêts à gérer le dépôt GitHub du projet SunRise__ :smiley: N'hésitez pas à relire les documents présents dans [docs](https://github.com/18tbr/sunrise-refonte/tree/tbr/docs) pour les avoir bien en mémoire lorsque vous ferez les revues de code.
