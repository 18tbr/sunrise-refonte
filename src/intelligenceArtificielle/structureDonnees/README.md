# structureDonnees

Ce dossier contient l'implémentation des `Arbres` RC utilisés pour représenter les modèles de thermique de bâtiment. Il contient aussi quelques données (exceptions et coefficients) qui sont utiles dans tout les fichiers.

## Les arbres RC

La représentation de circuit RC sous forme d'arbre est non triviale, mais elle est expliquée dans les diverses vidéeos préparées pour le cours de Mécatronique de 2020.

En dehors du sens de leur représentation, il est aussi important de comprendre certaines choses sur l'implémentation de ces arbres afin de pouvoir les manipuler correctement. Le point le plus important sur notre implémentation est que les arbres sont conçus pour maintenir toujours leur cohérence.

Les principales règles que les arbres vont chercher à maintenir sont :
 - Un objet `Feuille` est toujours une feuille de l'arbre
 - Un objet `Parallele` ou `Serie` n'est jamais une feuille de l'arbre et a toujours au moins deux fils
 - Les données sur l'arbre (forme, nombre de capacités etc...) doivent toujours être à jour

Prenons un exemple pour illustrer ce propos. Considérons l'arbre `individu` suivant :
```
    __sA__
   /      \
  pB      f1
 /  \
f3  f2
```
Si l'on tente d'ajouter un fils à `f1`, l'arbre va changer de forme (suivant ce qui aura été indiqué) pour que `f1` reste bien en feuille de l'abre. Par exemple :
```python
f4 = Feuille()
f1.ajoutFils(f4, forme="serie")
```
Va transformer `individu` en :
```
    __sA__
   /      \
  pB      sC
 /  \    /  \
f3  f2  f4  f1
```
De la même façon, (mais moins intuitif), si on tente de supprimer un fils à `pB`, par exemple avec :
```python
pB.suppressionFils(index=1)
```
Alors `individu` sera transformé en :
```
    __sA__
   /      \
  f2      sC
         /  \
        f4  f1
```
Comprendre cela devrait suffire à cerner comment manipuler toutes les données correctement.

## Arbre

Ce fichier contient l'implémentation des arbres qui servent de modèles simplifiés de thermique de bâtiment.

Les méthodes et attributs principaux de cette classe sont :
 - `simulation` : Réalise la simulation thermique avec le modèle proposé dans cet arbre
 - `score` : Renvoie le score de l'arbre (calculé en faisant la simulation numérique)
 - `inspecter` : Renvoie le noeud de profondeur et d'indice souhaité (trouvé par un parcours en largeur)
 - `ecritureImage` : Renvoie la représentation de l'arbre sous forme d'image
 - `lectureImage` : Met à jour les coefficents de l'arbre à partir de ceux de l'image
 - `normalisationImage` : Normalise une image pour lui rendre une forme avant de l'envoyer dans un autoencodeur
 - `forme` : Un attribut contenant la forme de l'image (_i.e._ le nombre de noeuds à chaque profondeur)

## Noeud

Ce fichier contient la classe abstraite éponyme représentant un noeud des arbres RC représentés. Les classes `Feuille`, `Parallele` et `Serie` héritent toutes de `Noeud`.

Les méthodes de la classe `Noeud` sont presques toutes liées à l'implémentation des arbres RC, donc à moins de rentrer dans le détail de l'implémentation des arbres RC il n'est pas très pertinent de les lister ici.

### Feuille

Ce fichier contient la classe `Feuille` qui hérite de `Noeud` et représente une feuille de l'arbre RC, c'est à dire une résistance.

### Parallele

Le fichier `Parallele` contient la classe eponyme qui représente une liaison série dans l'arbre RC.

C'est une blague, il faudrait vraiment être maléfique pour faire ça. La classe `Parallele` représente une liaison parallèle dans le circuit RC.

### Serie

Ce fichier contient l'implémentation des liaisons série dans l'arbre RC.

## Coefficients

Ce fichier sert de référence pour toutes les valeurs des coefficients. Il est utilisé dans les différents noeuds de l'arbre pour initialiser les nouveaux coefficients de façon aléatoire. La loi aléatoire suivie par ces coefficients peut être modifiée en changeant des valeurs globales définies dans le fichier.

Les fonction principales définies dans ce fichier sont :
 - `conductance` : Renvoie un coefficient de transmission H aléatoire en suivant une loi normale
 - `capacite` : Renvoie une valeur de capacité aléatoire en suivant une loi normale

## SunRiseException

Ce fichier définit un certain nombre d'exceptions spécifiques au projet qui peuvent être lancées par diverses parties du code.
