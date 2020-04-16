#!/usr/bin/python3
import os
import sys
import json
from subprocess import run

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
    if not os.path.exists(".identifiant"):
        print("Vous devez utiliser identifiant au moins une fois avant de pouvoir faire des modifications de code.", file=sys.stderr)
        return 1
    with open(".identifiant", 'r') as branchFile:
        branch = branchFile.read();
    gitProcess = run(f"git checkout {branch}", shell=True)
    if gitProcess.returncode != 0:
        print("---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?", file=sys.stderr)
        return 1
    # else...
    gitProcess = run("git pull origin master", shell=True)
    if gitProcess.returncode != 0:
        print("---X Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider.", file=sys.stderr)
        return 1
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
        return 1
    # else...
    gitProcess = run(f"git pull --rebase origin {nomBranche}", shell=True)
    if gitProcess.returncode != 0:
        print("---X Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider.", file=sys.stderr)
        return 1
    # else...
    print(f"---> Fusion de {nomBranche} effectuée avec succès")
    return 0

def nouveau():

    pass

def info():
    data = {}
    # nom de la tâche
    data["nom"] = input("Nom de la tâche :\n>> ")
    # nom du groupe
    groupe = input("Nom du groupe :\n>> ")
    while group not in ["UI", "AI", "Arduino", "Simulation", "Grille", "SunRise", "Arduino", "DevOps"]:
        print("Le nom de groupe rentré n'est pas reconnu. Les noms de groupe possibles sont : 'UI', 'AI', 'Arduino', 'Simulation', 'Grille', 'SunRise', 'Arduino', et 'DevOps'.", file=sys.stderr)
        groupe = input("Nom du groupe :\n>> ")
    data["groupe"] = groupe
    # type de la tâche
    typeTache = input("Type de la tâche :\n>> ")
    while typeTache not in ["general", "code"]:
        print("Le type de tâche rentré n'est pas reconnu. Les 2 types de tâches possibles sont 'general' (pour une tâche générale) et 'code' (pour une fonction ou méthode).", file=sys.stderr)
        typeTache = input("Type de la tâche :\n>> ")
    data["type"] = typeTache

    if data["type"] == "general":
        # description
        data["desc"] = input("Description de la tâche :\n>> ")
        # état
        etat = input("Etat de la tâche :\n>> ")
        while etat not in ["incomplet", "complet"]:
            print("L'état rentré n'est pas reconnu. Les états possibles pour une tâche sont 'incomplet' et 'complet'.", file=sys.stderr)
            etat = input("Etat de la tâche :\n>> ")
        # rapport




    else:  # code
        pass
    pass


if __name__ == '__main__':
    fusion()
