# src

Ce dossier contient le code source du projet et il est __organisé en plusieurs sous dossiers__ qui séparent les __différents niveaux d'abstraction__ du code. Ce dossier continent __l'implémentation de l'interface graphique__ du projet.

## Organisation de src

Le code source dans src est séparé en trois morceaux prinipaux :
 - L'implémentation de __l'interface graphique__
 - L'implémentation de __l'algorithme génétique__ et du machine learning
 - L'implémentation des arbres et des __structures de données__ utiles pour le reste du code

L'organisation du dépôt src à l'heure actuelle peut être résumée comme suit :

```bash
src
|__ "Implémentation de l'interface Graphique"
|__ "Implémentation des pages de l'interface Graphique"
|__ intelligenceArtificielle
    |__ "Implémentation de l'algorithme génétique"
    |__ "Implémentation des autoencodeurs"
    |__ structureDonnees
	|__ "Implémentation des arbres RC"
	|__ "Implémentation des noeuds des arbres RC"
```

Le contenu de chacune de ces implémentations est __détaillé dans le README du dossier dédié__.

## Système d'imports

Etant donné la structure assez délicate du code dans ce dépôt (imposée par sa taille), __le système pour importer des fichiers n'est pas aussi trivial qu'en temps normal__. Pour que les imports restent assez simple, on fait toujours l'hypothèse que le __dossier src__ se trouve dans le _PYTHONPATH_, c'est à dire que le contenu du dossier src peut être importé directement.

```python
# Exemple d'import d'un fichier dans le module src
from InterfaceGraphique import InterfaceGraphique
```

En revanche, le fichiers qui se trouvent dans des modules plus profonds doivent être __importés en utilisant leur chemin relatif à src__.

```python
# On cherche à importer le module coefficient qui se trouve dans (src)/intelligenceArtificielle/structureDonnees/Coefficients en lui donnant le simple nom Coefficients
import intelligenceArtificielle/structureDonnees/Coefficient as Coefficients
```

Notez que le système d'imports actuel n'est pas optimal, on pourrait utiliser les fichiers \_\_init\_\_ des différents dossiers pour __ecapsuler les imports__.

## Interface Graphique

Ce dossier contient l'implémentation de __l'interface graphique de l'outil SunRise__. Cette implémentation est __structurée en pages__, c'est à dire que chaque page qui apparait visuellement sur l'outil dispose de sa propre classe dans ce dossier. Ces pages sont utilisées et reliées entre elles par l'interface graphique, qui est aussi une classe.

Notez que de manière générale, l'implémentation de l'interface graphique aujourd'hui n'est _pas de très bonne qualité_.

### InterfaceGraphique.py

Ce fichier contient l'implémentation de l'objet InterfaceGraphique qui va __créer l'interface graphique et gérer les différentes pages__ pour vous.

Les principales méthodes de cet objet sont :
 - afficher : sert à afficher l'interface graphique à l'utilisateur
 - pageSuivante : est appelé par une page de l'interface graphique pour signifier que l'interation avec l'utilisateur est terminée et que l'on doit passer à la page suivante

### PageLectureDonnees

Ce fichier contient l'implémentation de l'objet PageLectureDonnees. Cet objet représente la première page de l'interface graphique, dans laquelle l'utilisateur rentre les courbes de mesure.

### PageLectureConfiguration

Ce fichier contient l'implémentation d'une classe éponyme qui représente la deuxième page de l'interface graphique. C'est dans cette page que l'utilisateur rentre les différents paramètres de l'algorithme de machine learning. Notez que __la façon dont cette page interagit avec l'utilisateur n'est pas du tout optimale__. Un façon plus agréalble pour l'utilisateur serait de pouvoir rentrer toute la configuration de l'algorithme avec un fichier json (par exemple) et de choisir le modèle à utiliser avec son explorateur de fichiers.

### PageAnimation

Ce fichier contient l'implémentation de la troisième page de l'interface graphique, celle sur laquelle l'utilisateur peut suivre en temps réel l'évolution de l'algorithme. Il s'agit d'une certaine façon juste d'une __barre de chargement glorifiée__. De toutes les parties de l'interface graphique, c'est sans doute celle qui a __l'implémentation la plus douteuse__.

Le temps de pause au début du lancement de la troisième page correspond au __temps de chargement par keras du fichier md5__ spécifié par l'utilisateur.

### PageResultats

Ce fichier contient la dernière page de l'interface graphique. Les deux informations visibles sur cette page sont une courbe permettant de comparer l'entrée-sortie obtenue par le meilleur circuit de l'algorithme à la référence, et une seconde courbe sur l'erreur des différents individus de la population.

Notez que __cette second courbe est parfaitement inutile__, nous l'avons mise ici juste pour remplir l'espace pour la démonstration au Forum de Mécatronique 2020. __Ce que vous voudrez sans doute afficher__ à cet endroit à la place de cette courbe sont deux courbes donnant la __répartition des coefficients RC obtenus dans la population ponderée par le score des individus__. Ces courbes fourniront une idée plus fine des paramètres d'intérêt recherchés.
