# src
C'est ici que sont décrites si besoin les méthodes utilisées dans les codes du dossier `src`.

# Autoencodeurs

## Entrainement supervisé et non supervisé

Pour comprendre la méthode employée ici, il faut comprendre ce dont est capable un autoencodeur classique. Une utilisation fréquente d'un autoencodeur est de prendre une image en input, et de renvoyer cette image __de la manière la plus fidèle possible__. La fonction de "score" utilisée pour évaluer la pertinence d'un output se doit d'être __différentiable__, afin de permettre à l'autoencodeur de réaliser la rétropropagation du gradient nécessaire à la mise à jour des poids du réseau.

Ici, on souhaite écrire un autoencodeur qui prenne en entrée une image (représentant un arbre) et qui renvoie une version "brouillée" __améliorée__ de cette image. Le score d'un output est calculé en faisant la simulation numérique du circuit électrique, et passer de l'image au score n'est pas une opération différentiable ! L'entraînement non supervisé est donc __impossible__.

:raised_hand: _Comment alors entraîner l'autoencodeur ?_

Comme l'a dit un grand penseur,
> Comme beaucoup de problèmes, cela peut se résoudre si l'on fait absolument n'importe quoi :+1:

On va donc pour cela entraîner notre autoencodeur de manière __supervisée__, en permettant à l'autoencodeur de disposer d'une erreur sur chacun des poids du réseau et de pouvoir ensuite rétropropager. Pour cela, il faudrait __pour chaque arbre en entrée disposer d'un arbre plus performant__, que l'on comparera avec la sortie du réseau pour évaluer sa pertinence :ok_hand:

## Entrainement de l'autoencodeur initial

Il nous faut donc maintenant générer pour chaque arbre un arbre légèrement meilleur. Pour cela, nous utilisons un __Variational Autoencodeur__ (VAE). Il jouera le rôle d'un autoencodeur qui prend une image en entrée et qui essaie de renvoyer la même image en sortie ; comme nous avons vu plus haut, la fonction de "score" est différentiable et ce VAE est donc entraînable de manière __non supervisée__. L'astuce est que la sortie du VAE est soumise à une perturbation aléatoire, ce qui fait que l'on pourra produire pour chaque arbre une dizaine (ou plus) d'images différentes grâce à ce VAE, toutes ayant des scores différents. Certains auront un score moins bon, d'autres un meilleur score. Il nous suffira alors de sélectionner __la meilleure image__ parmi celles obtenues. L'autoencodeur entraîné ainsi sera capable de réaliser de façon déterministe l'amélioration qui était trouvé de façon non déterministe par le VAE.

__On a donc ce qu'il nous faut pour entraîner notre autoencodeur__ :heavy_check_mark:

## Amélioration itérative de l'autoencodeur

Cela étant, l'autoencodeur entraîné ainsi (nommé AE1 dans la suite) n'est pas très performant. Pour être précis, __AE1 est à peine meilleur que le hasard__ pour améliorer les coefficients de nos arbres (mais il a le grand mérite d'être déterministe). Si on veut que la convergence de notre algorithme ne soit pas trop longue, il nous faut __utiliser un autoencodeur de meilleure qualité__. Il nous faut donc trouver un moyen de construire un autoencodeur performant à partir de AE1.

L'idée de la construction de ce nouvel autoencodeur est très simple : si AE1 est capable de prendre un arbre en entrée et de renvoyer un arbre un peu meilleur en sortie, alors __appliquer AE1 une seconde fois__ sur l'arbre en sortie permettra d'obtenir un troisième arbre encore plus performant. On peut alors entrainer un nouvel autoencodeur AE2 en lui donnant en entrée l'arbre initial et en sortie le troisième arbre.

L'avantage de cette méthode est qu'elle permet de __construire itérativement notre autoencodeur__ en augmentant (avec une vitesse en théorie géométrique, en pratique sans doute faible) l'efficacité de l'autoencodeur au fil des générations.

## Normalisation

Un détail technique d'implémentation cependant : lire et relire les images afin de créer des arbres est assez long, donc pour accélérer cet entrainement nos arbres disposent d'une __méthode de normalisation__ permettant de modifier l'image en place sans faire de lecture écriture couteuse.

> Pourquoi normaliser les images et ne pas directement apprendre par exemple à AE2 à faire AE1 o AE1 ?

### Formulation simple

Le problème est que __AE1 a été entrainé sur des images qui ne sont pas quelconques__, ce sont des images d'arbre qui ont une forme. En revanche lors de sa reconstruction d'une image, __AE1 ne va pas respecter la forme de l'image__ et va au contraire tout flouter. Par suite, on ne peut pas composer AE1 par AE1 directement sans avoir des problèmes.

### Formulation mathématique

Pour formuler cela d'une façon plus mathématique, si on considère __E l'ensemble des images possibles__ et l'ensemble des images qui sont des __images d'arbre bien formées F__, on voit que F est inclut dans E mais E n'est pas égal à F.

AE1 a été entrainé sur des images qui sont toutes dans F, et il est capable de les améliorer. Donc __AE1 est un opérateur défini de F sur E comme améliorant les images__. La confusion vient du fait que l'autoencodeur est en pratique capable de réaliser des calculs sur toutes les images sans rencontrer d'erreur au sens informatique. Cela signifie qu'en réalité la fonction AE1 est valuée de tout E dans tout E. Mais __rien ne laisse supposer que AE1 est bien améliorant sur E/F__ (en fait ce n'est probablement pas le cas).

Ainsi, si on veut que AE1 améliore le score d'une image, il faut forcément que cette image se trouve dans l'espace F. Pour passer une image de E dans F, on définit pour tout arbre A __l'opérateur de normalisation NA__ (non injectif) qui à une image dans E associe une image dans F.

Ainsi, __AE2 sera entrainé à imiter des opérateurs de la forme AE1 o NA o AE1__ qui sont à valeur de F dans E. L'abre utilisé pour faire chaque normalisation est celui utilisé pour créer l'image en premier lieu.

## Pseudo code

On propose ci dessous un pseudo-code (en python) pour __expliciter l'entrainement__ que nous avons décrit ci dessus. Notez que le pseudo code python écrit ci dessous n'est __pas contractuel du code vraiment utilisé__ (les noms de méthodes ne sont pas forcément les mêmes par exemple et toutes les variables ne sont pas définies rigoureusement).

Le pseudo code de l'entrainement de l'autoencodeur est :

```python
# On commence par créer le VAE
populationInitiale = arbresAleatoires(nombre)
VAE = nouvelAutoEncodeurVariationnel()
VAE.entrainementNonSupervise(populationInitiale)

# Une fois le VAE créé, on entraine AE1 avec VAE
populationInitiale = arbresAleatoires(nombre)
populationFinale = VAE.ameliorerNonDeterministe(populationInitiale)
AE1 = nouvelAutoEncodeur()
AE1.entrainementSupervise(populationInitiale, populationFinale)

# Maintenant que l'on dispose d'un autoencodeur déterministe permettant d'améliorer notre population, on peut itérativement créer notre meilleur autoencodeur
AEActuel = AE1
for iteration in range(nombreIterationsSouhaite):
  # On génère une population aléatoire
  populationInitiale = arbresAleatoires(nombre)
  # On améliore avec un autoencodeur déterministe
  populationIntermediaire = AEActuel.ameliorer(populationInitiale)
  # On normalise notre population pour rester dans le bon espace
  populationIntermediaire.normaliser()
  # On améliore une seconde fois la population
  populationFinale = AEActuel.ameliorer(populationFinale)
  # On entraine un nouvel autoencodeur à reproduire ces étapes de façon déterministe
  AEFutur = nouvelAutoEncodeur()
  AEFutur.entrainementSupervise(populationInitiale, populationFinale)
  AEActuel = AEFutur

return AEActuel
```
