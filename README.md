[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python application](https://github.com/18tbr/sunrise-refonte/workflows/Python%20application/badge.svg)
[![PyPI version](https://badge.fury.io/py/sunriseces.svg)](https://pypi.org/project/sunriseces/)
[![License](https://img.shields.io/github/license/18tbr/sunrise-refonte)](https://github.com/18tbr/sunrise-refonte/blob/master/LICENSE)
![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)
![Linux Support](https://img.shields.io/badge/Linux-Support-brightgreen.svg)
![Mines de Paris](https://img.shields.io/badge/Organisme-Mines%20de%20Paris-blue)
# Mines de Paris - CES
Le dépôt GitHub pour le projet SunRise de 2020.

<p align="center">
    <a href="https://sites.google.com/view/2019-2020-gr12/home" target="_blank">
        <img src="https://github.com/18tbr/sunrise-refonte/blob/master/assets/logoProjet2020.png?raw=true" height="250px">
    </a>
</p>

## Le projet SunRise
Le projet SunRise est un projet lancé en 2017 par le [CES](http://www.ces.mines-paristech.fr/Accueil/) (Centre d'Efficacité des Systèmes) des [Mines de Paris](http://www.mines-paristech.fr/). Ce projet a pour but de __valider des modèles novateurs de thermique :fire: de bâtiment :house:__ du CES à l'aide d'une expérience en chambre climatique.

Une particularité de l'expérience du CES (qui donne son nom au projet) est qu'elle utilise un __soleil :sunny: artificiel mobile de grande dimension__ (~2m de diamètre) afin de bénéficier de davantage de flexibilité lors de l'évaluation de l'influence des rayons lumineux :flashlight:

Pour plus de détails, vous pouvez visiter le [site du projet](https://sites.google.com/view/2019-2020-gr12/home) :point_left: ou même la [vidéo de présentation du projet](https://youtu.be/zrpTuERl-vk) :movie_camera:

## Ce dépôt
Ce dépôt contient le travail d'une équipe d'étudiants des Mines de Paris sur une __méthode d'identification de paramètres d'intérêt__ :monocle_face: à partir de mesures de thermique de bâtiment. Il s'agit d'un élément préalable à la réalisation de l'expérience SunRise.

La méthode développée ici est inhabituelle, et l'algorithme proposé tente de fournir une solution à l'inférence de paramètres en utilisant des __méthodes de Machine Learning__ :robot:

![SunRise démo](assets/demo.gif)

## Package Python

Ce projet utilise l'outil [Poetry](https://python-poetry.org) pour gérer les dépendances et faire un package pip utilisable plus facilement. Le package pip du projet se nomme [sunriseces](https://pypi.org/project/sunriseces/).

Pour installer le package, vous pouvez donc utiliser :

```sh
# Si pip se trouve dans votre PATH
pip install sunriseces

# Sinon sous Linux
python3 -m pip install sunriseces

# De même sous Windows
python -m pip install sunriseces
```

Une fois le package installé, vous pourrez utiliser l'outil graphique en utilisant l'une des commandes :

```sh
# Si le dossier des modules exécutables python se trouve dans votre PATH
sunrise

# Sinon sous Linux
python3 -m sunrise

# De même sous Windows
python -m sunrise
```

## Contribution
Si vous __souhaitez contribuer à ce dépôt :heart:__, nous vous invitons à consulter les différents documents du [dossier docs](https://github.com/18tbr/sunrise-refonte/tree/master/docs) qui détaillent les façons de contribuer au projet, les conventions de nommage, etc...

## Vidéos de travail

Un certain nombre de __vidéos :movie_camera: ont été filmées pendant la conception du code source__. Même si elles ne sont __plus forcément en phase avec l'implémentation__, elles permettent sans doute de __comprendre :bulb: le principe de l'outil__ et _certaines subtilités de son implémentation_.

Toutes les vidéos de travail sont disponible publiquement :+1: sous la licence "_Creative Commons_" sur [YouTube](https://www.youtube.com/channel/UCJJFF_SMw4H7YDuy-jOA1-Q).

## License
Le code de ce dépôt est _sauf contre-indication_ mis à disposition sous license [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).

<p align="center">
  <a href="http://www.mines-paristech.fr/" target="_blank">
      <img src="https://github.com/18tbr/sunrise-refonte/blob/master/assets/logoMinesParisTech.png?raw=true" height="100px">
  </a>
</p>

<p align="center">
  <a href="http://www.ces.mines-paristech.fr/Accueil/" target="_blank">
      <img src="https://github.com/18tbr/sunrise-refonte/blob/master/assets/logoCES.png?raw=true" height="75px">
  </a>
</p>
