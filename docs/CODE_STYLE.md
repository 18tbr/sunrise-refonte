# Conventions d'écritures

Ce fichier est destiné à toutes personne souhaitant contribuer au projet en participant à l'écriture du code, mais il pourra aussi être utile à quelqu'un qui cherche juste à comprendre le code en lisant. __Le présent document détaille les conventions d'écritures et de nommages utilisées à travers le projet__.

> :raised_hand: Pourquoi forcer une convention d'écriture au lieu de laisser les
> contributeurs faire ce qu'ils veulent ?

Le fait de ne pas respecter la convention d'écriture ne créera pas d'erreurs de code ou de syntaxe, et **python ne fera pas de commentaires sur votre style**. En revanche, le fait d'avoir une unique convention pour le projet permet de le rendre **plus rapide à relire et à comprendre**. Cela accélère sensiblement le processus de revue de code :ok_hand:

## Les règles à respecter

1. ### Les objets

  Les noms d'objets (i.e. de classes) doivent suivre la convention de nommage dite __Pascal Case__, c'est à dire que tous les mots qui composent le nom de la classe doivent être collés et avoir une première lettre en capital. Par exemple __NomDeClasse__ est bien du Pascal Case, tandis que ~~nomDeClasse~~ et ~~Nom_De_Classe~~ ne sont pas du Pascal Case.

2. ### Les fonctions, méthodes et variables

  Les fonctions, méthodes et variables suivent toutes la même convention de nommage, dite __Camel Case__. Le Camel Case est identique au Pascal Case si ce n'est que la première lettre du nom n'est pas capitalisée. Par exemple, __nomDeVariable__ est bien du Camel Case, tandis que ~~NomDeVariable~~ et ~~Nom_De_Variable~~ n'en sont pas.

3. ### Les constantes _(Convention optionnelle)_

  Pour souligner qu'une variable contient une constante immutable du programme (au sens du const du C par exemple), un contributeur peut nommer cette variable en suivant la convention dite __Macro Case__, c'est à dire en mettant tous les mots qui composent le nom de la variable en majuscule et en les reliant par des underscores "\_". Par exemple, __NOM\_DE\_CONSTANTE__ est bien du Macro Case, tandis que ~~Nom_De_Constante~~ et ~~NOMDECONSTANTE~~ n'en sont pas.

4. ### Le language

  A travers tout le projet, les __noms de variables__, __noms de fonctions__, __noms d'objets__, __noms de fichiers__, __commentaires__ et __chaînes de caractères__ doivent toujours être écrites __en français__. Cela n'est pas toujours intuitif mais permet à des contributeurs peu anglophones de participer au projet plus facilement :+1: Toutes fonctions et variables définies dans d'autres librairies sont évidemment utilisées en anglais.

5. ### Formatage de code

  Le formatage du code du projet est assuré par l'outil `black` de la PSF (Python Software Foundation). L'objectif de taille de ligne est :point_right: __80 caractères par ligne__. Il est permis d'avoir plus de 80 caractères sur une ligne pour des commentaires ou une longue chaîne de caractères dans la mesure où black n'est pas capable de corriger cela seul (à l'heure actuelle :pray:).

6. ### Conseils _(Conventions optionnelles)_

  Les éléments dans cette section ne sont que des conseils pour vous aider à écrire un code plus simple, vous n'êtes pas forcés de les suivre :v: La première chose est de penser à utiliser les __capacités de pattern matching__ de Python. Le premier cas est que si une fonction `f` renvoie (par exemple) trois arguments, vous pouvez récupérer les trois arguments avec :
  ```python
  a, b, c = f()
  ```
  De la même façon, si `L` est une liste avec trois éléments, vous pouvez les récuperer avec la syntaxe :
  ```python
  a, b, c = L
  ```
  Cette syntaxe est particulièrement utile pour récupérer les fils d'un arbre lorsque vous écrivez des tests.

  Nhésitez pas à utiliser des __décorateurs__ dans vos objets. S'ils sont assez pénalisants en termes de performances, il n'empèche que ces décorateurs rendent le code beaucoup plus lisible et simple à modifier. Les principaux décorateurs qui pourront vous êtres utiles sont `\@property` et `\@item.setter`.
