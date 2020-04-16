#!/usr/bin/python3
import os
import sys
from subprocess import run
from pathlib import Path

def main():
    print("---! Ceci est le script d'intégration continue.\nIl n'est pas encore prêt à être utilisé.")
    input("Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n"
    ">> identifiant"
    )

def identifiant():
    prenomId = input("Identifiant :\n>> ")
    with open(".identifiant", 'w') as idFile:
        idFile.write(prenomId)
    print("---> Mise à jour effectuée avec succès")
    return 0

def maj():
    branch = ""
    with open(".identifiant", 'r') as branchFile:
        branch = branchFile.read();
    gitProcess = run(f"git checkout {branch}", shell=True)
    if gitProcess.returncode != 0:
        print("---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?", file=sys.stderr)
    # else...
    gitProcess = run("git pull origin master", shell=True)
    if gitProcess.returncode != 0:
        print("---X Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider.", file=sys.stderr)
    # else...
    print("---> Mise à jour effectuée avec succès")
    return 0

def fini():
    pass

def statut():
    pass

def groupe():
    nomGroupe = input("Nom du groupe à créer :\n>> ")
    nomRepertoire = os.path.join("taches", nomGroupe)
    os.makedirs(nomRepertoire, exist_ok=True)
    print("---> Mise à jour effectuée avec succès")
    return 0

def fusion():
    nomBranche = input("Nom de la branche à fusionner :\n>> ")
    gitProcess = run("git checkout master", shell=True)
    if gitProcess.returncode != 0:
        print("---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?", file=sys.stderr)
    # else...
    gitProcess = run(f"git pull --rebase origin {nomBranche}", shell=True)
    if gitProcess.returncode != 0:
        print("---X Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider.", file=sys.stderr)
    # else...
    print(f"---> Fusion de {nomBranche} effectuée avec succès")
    return 0

def nouveau():
    pass

def info():
    pass


if __name__ == '__main__':
    fusion()
