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
    Path(".identifiant").touch(exist_ok=True)
    with open(".identifiant", 'w') as idFile:
        idFile.write(prenomId)
    print("---> Identifiant stocké avec succès")
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
    # Ajout de tout le travail fait depuis le dernier commit
    gitProcess = run("git add .", shell=True)
    if gitProcess.returncode != 0:
        print("---X Le travail que vous avez fait n'a pas pu être ajouté. Demandez de l'aide au groupe DevOps pour régler le problème.", file=sys.stderr)
        return 1
    # Récupération du texte du rapport
    open("message_ci_tmp", 'w').close()
    print("---> Inscrivez une phrase de rapport dans votre éditeur de texte")
    editor = ""
    if sys.platform == 'linux':
        editor = "nano"
    elif sys.platform == 'win32':
        editor = "notepad.exe"
    else:
        print(f"Votre plateforme {sys.platform} n'est pas supportée.", shell=True)
        return 1

    textProcess = run(f"{editor} message_ci_tmp", shell=True)
    if textProcess.returncode != 0:
        print("---X Une erreur est surnvenue pendant que vous rentriez votre message, ce dernier n'a pas été validé. Vous devez utiliser fini à nouveau pour valider votre travail.", file=sys.stderr)
        return 1
    # else...
    # Lecture du message enregistré
    message = ""
    with open("message_ci_tmp", 'r') as messageFile:
        message = messageFile.read()
    # Validation du travail effectué
    gitProcess = run(f"git commit -m \"{message}\"", shell=True)
    if gitProcess.returncode != 0:
        print("---X Le travail que vous avez fait n'a pas pu être validé. Demandez de l'aide au groupe DevOps pour régler le problème.", file=sys.stderr)
        return 1
    # Envoi du travail effectué
    gitProcess = run(f"git push", shell=True)
    if gitProcess.returncode != 0:
        print("---X Le travail que vous avez fait n'a pas pu être enregisté. Demandez de l'aide au groupe DevOps pour régler le problème.", file=sys.stderr)
        return 1
    print("---> Votre travail a bien été enregistré.")
    return 0



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
    pass


if __name__ == '__main__':
    fusion()
