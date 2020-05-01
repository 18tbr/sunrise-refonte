# Types de contributions

Ce dépôt fait partie du projet SunRise, donc deux cas de figure se posent si vous voulez contribuer à ce travail :
 - Vous faites partie du projet SunRise
 - Vous êtes extérieur au projet SunRise

## Vous faites partie du projet SunRise

Si vous faites partie du projet SunRise, pour contribuer au projet vous devrez utiliser l'outil ci.py fourni dans ce dépôt. Pour cela, il faut que le mainteneur du dépôt vous ajoute aux contributeurs du projet. La première chose à faire est donc de contacter le groupe DevOps qui gère l'intégration continue sur ce dépôt.

Une fois que le groupe DevOps aura préparé votre arrivé, vous devrez cloner ce dépôt en utilisant git :

> $ git clone https://github.com/18tbr/sunrise-refonte.git


La suite du travail se fera avec l'outil ci.py, qui ne fonctionne qu'avec une version de python >= 3.5. Pour vérifier si vous avez une installation de python qui convient, vous pouvez utiliser :

Sous Windows
> $ python --version

Sous Linux
> $ python3 --version

Une fois le dépôt cloné, il vous faudra vous identifier sur le dépôt. Vous n'aurez besoin de réaliser cela qu'une seule fois. La commande à utiliser est :

> $ cd sunrise-refonte <br>
> $ python ./ci.py identifiant

L'outil ci.py vous demandera alors votre identifiant, qui est celui que le groupe DevOps vous aura donné. Si vous ne parvenez pas à vous identifier, contactez le groupe DevOps.

Une fois votre authentification réussie, vous n'aurez plus que deux commandes à retenir pour pouvoir contribuer au projet.

En début de séance de travail, vous devez mettre à jour le code sur votre PC par rapport au code sur GitHub. Pour cela, utilisez :

> $ python ./ci.py maj

Une fois la mise à jour effectuée, vous pourrez commencer votre travail. Modifiez vos fichiers comme vous le feriez en temps normal, puis à la fin de votre travail vous devez envoyer vos modifications sur GitHub. Pour cela, utilisez la commande :

> $ python ./ci.py fini

L'outil ouvrira alors un éditeur de texte (sans doute notepad.exe) sur lequel vous devrez inscrire un court message descriptif résumant les modifications que vous avez réalisées. Lorsque vous fermerez votre éditeur de texte, le message sera enregistré et votre travail envoyé sur GitHub.

## Vous êtes extérieur au projet SunRise

Les consignes de contribution au dépôt pour les gens ne faisant pas partie du projet ne sont pas clairement définies. Pour savoir comment vous pouvez contribuer au dépôt, contactez le groupe DevOps en charge ou bien le mainteneur du dépôt.
