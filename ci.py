#!/usr/bin/python3
import os
import sys
from subprocess import run
from pathlib import Path


if __name__ == '__main__':
    main()

def main():
    print("---! Ceci est le script d'intégration continue.\nIl n'est pas encore prêt à être utilisé.")
    input("Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n"
    ">> identifiant"
    )

def identifiant():
    prenomId = input("Identifiant ?\n")
    Path(".identifiant").touch(exist_ok=True)

def maj():
    pass

def fini():
    pass

def statut():
    pass

def groupe():
    nomGroupe = input("Nom du groupe à créer ?\n")
    nomRepertoire = os.path.join("taches", nomGroupe)
    os.makedirs(nomRepertoire, exist_ok=True)

def fusion():
    pass

def nouveau():
    pass

def info():
    pass
