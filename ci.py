#!/usr/bin/python3
import os
import sys
from subprocess import run


if __name__ == '__main__':
    maj()

def main():
    print("---! Ceci est le script d'intégration continue.\nIl n'est pas encore prêt à être utilisé.")
    input("Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n"
    ">> identifiant"
    )

def identifiant():
    pass

def maj():
    branch = ""
    with open(".identifiant", 'r') as branchFile:
        branch = branchFile.read();
    gitProcess = run(f"git checkout {branch}", shell=True)
    if gitProcess.returncode != 0:
        print("---X git n'a pas pu être lancé correctement.\nEtes-vous certain que git est bien accessible ?", file=sys.stderr)
    # else...
    gitProcess = run(f"git pull origin master", shell=True)
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
    pass

def fusion():
    pass

def nouveau():
    pass

def info():
    pass
