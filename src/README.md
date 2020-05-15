# src
C'est ici que sont décrites si besoin les méthodes utilisées dans les codes du dossier `src`.

## Autoencoders
Pour comprendre la méthode employée ici, il faut comprendre ce dont est capable un autoencoder classique. Une utilisation fréquente d'un autoencoder est de prendre une image en input, et de renvoyer cette image __de la manière la plus fidèle possible__. La fonction de "score" utilisée pour évaluer la pertinence d'un output se doit d'être __différentiable__, afin de permettre à l'autoencoder de réaliser la rétropropagation du gradient nécessaire à la mise à jour des poids du réseau.

Ici, on souhaite écrire un autoencoder qui prenne en entrée une image (représentant un arbre) et qui renvoie une version "brouillée" __améliorée__ de cette image. Le score d'un output est calculé en faisant la simulation numérique du circuit électrique, et passer de l'image au score n'est pas une opération différentiable ! L'entraînement non supervisé est donc __impossible__.

:raised_hand: _Comment alors entraîner l'autoencoder ?_

Comme l'a dit un grand penseur,
> Comme beaucoup de problèmes, cela peut se résoudre si l'on fait absolument n'importe quoi :+1:

On va donc pour cela entraîner notre autoencoder de manière __supervisée__, en permettant à l'autoencoder de disposer d'une erreur sur chacun des poids du réseau et de pouvoir ensuite rétropropager. Pour cela, il faudrait __pour chaque arbre en entrée disposer d'un arbre plus performant__, que l'on comparera avec la sortie du réseau pour évaluer sa pertinence :ok_hand:

Il nous faut donc maintenant générer pour chaque arbre un arbre légèrement meilleur. Pour cela, nous utilisons un __Variational Autoencoder__ (VAE). Il jouera le rôle d'un autoencoder qui prend une image en entrée et qui essaie de renvoyer la même image en sortie ; comme nous avons vu plus haut, la fonction de "score" est différentiable et ce VAE est donc entraînable de manière __non supervisée__. L'astuce est que la sortie du VAE est soumise à une perturbation aléatoire, ce qui fait que l'on pourra produire pour chaque arbre une dizaine (ou plus) d'images différentes grâce à ce VAE, toutes ayant des scores différents. Certains auront un score moins bon, d'autres un meilleur score. Il nous suffira alors de sélectionner __la meilleure image__ parmi celles obtenues.

__On a donc ce qu'il nous faut pour entraîner notre autoencoder__ :heavy_check_mark:
