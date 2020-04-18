#!/usr/bin/python3
import os
import sys
import json
from subprocess import run, DEVNULL


def main(richInput):
    print(
        "\n---! Ceci est le script d'intégration continue.\n---! Il n'est pas encore prêt à être utilisé.\n"
    )
    demande = richInput.wideInput(
        "Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n---- identifiant\n---- maj\n---- fini\n\nVotre demande :\n>> "
    )
    while demande not in [
        "identifiant",
        "maj",
        "fini",
        "fusion",
    ]:
        print(
            f"Votre demande {demande} n'a pas été comprise, vous ne pouvez utiliser que l'une des demandes proposées."
        )
        demande = richInput.wideInput(
            "Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n---- identifiant\n---- maj\n---- fini\n\nVotre demande :\n>> "
        )

    print()  # A blank line for the style :-)
    if demande == "identifiant":
        identifiant(richInput)
    elif demande == "maj":
        maj(richInput)
    elif demande == "fini":
        fini(richInput)
    elif demande == "fusion":
        fusion(richInput)


def identifiant(richInput):
    listePrenoms = [
        "theo",
        "tbr",
        "thibault",
        "pierre",
        "maud",
        "lucie",
        "alicia",
        "camille",
        "arthur",
        "vitor",
        "felipe",
        "litao",
        "martin",
        "shao-hen",
    ]
    print("Les identifiants possibles sont :\n")
    for prenom in listePrenoms:
        print(f"---- {prenom}")
    print("\n")
    prenomId = richInput.wideInput("Identifiant :\n>> ")
    while prenomId not in listePrenoms:
        print(
            "L'identifiant que vous avez rentré n'est pas valable, veuillez rentrer un des identifiants possibles.",
            file=stderr,
        )
        print("Les identifiants possibles sont :\n")
        for prenom in listePrenoms:
            print(f"---- {prenom}")
        print("\n")
    with open(".identifiant", "w") as idFile:
        idFile.write(prenomId)
    print(
        f"---> Identification réalisée avec succès, bienvenue {prenomId.capitalize()} :-)"
    )


def maj(richInput):
    branch = richInput.user()
    gitProcess = run(f"git checkout {branch}", shell=True)
    if gitProcess.returncode != 0:
        print(
            "---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?",
            file=sys.stderr,
        )
        return 1
    # else...
    gitProcess = run("git pull origin master", shell=True)
    if gitProcess.returncode != 0:
        print(
            "---X Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider.",
            file=sys.stderr,
        )
        return 1
    # else...
    print("---> Mise à jour effectuée avec succès")


def fini(richInput):
    branch = richInput.user()
    # Récupération du groupe

    # Création d'un message de commit synthétique
    commit = richInput.editorInput(
        "---> Inscrivez votre rapport dans votre éditeur de texte",
        "",
    )
    messageCommit = (
        f"{branch} : {commit}."
    )

    gitProcess = run(f"git checkout {branch}", shell=True)
    if gitProcess.returncode != 0:
        print(
            "---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?",
            file=sys.stderr,
        )
        return 1
    # Ajout de tout le travail fait depuis le dernier commit
    gitProcess = run("git add .", shell=True)
    if gitProcess.returncode != 0:
        print(
            "---X Le travail que vous avez fait n'a pas pu être ajouté. Demandez de l'aide au groupe DevOps pour régler le problème.",
            file=sys.stderr,
        )
        return 1

    # Validation du travail effectué
    gitProcess = run(f'git commit -m "{messageCommit}"', shell=True)
    if gitProcess.returncode != 0:
        print(
            "---X Le travail que vous avez fait n'a pas pu être validé. Demandez de l'aide au groupe DevOps pour régler le problème.",
            file=sys.stderr,
        )
        return 1
    # Envoi du travail effectué
    gitProcess = run(f"git push", shell=True)
    if gitProcess.returncode != 0:
        print(
            "---X Le travail que vous avez fait n'a pas pu être enregisté. Demandez de l'aide au groupe DevOps pour régler le problème.",
            file=sys.stderr,
        )
        return 1
    print("---> Votre travail a bien été enregistré.")


def fusion(richInput):
    nomBranche = richInput.wideInput("Nom de la branche à fusionner :\n>> ")
    gitProcess = run("git checkout master", shell=True)
    if gitProcess.returncode != 0:
        print(
            "---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?",
            file=sys.stderr,
        )
        return 1
    # else...
    gitProcess = run(f"git pull --rebase origin {nomBranche}", shell=True)
    if gitProcess.returncode != 0:
        print(
            "---X Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider.",
            file=sys.stderr,
        )
        return 1
    # else...
    gitProcess = run(f"git push", shell=True)  # Pour mettre à jour le dépôt distant
    if gitProcess.returncode != 0:
        print(
            "---X Le push de la branche fusionnée a échoué. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider.",
            file=sys.stderr,
        )
        return 1
    print(f"---> Fusion de {nomBranche} effectuée avec succès")


# A class to handle various types of input
class RichInput(object):
    """docstring for RichInput."""

    def __init__(self):
        super(RichInput, self).__init__()
        self.cursor = 1

    def user(self):
        branch = ""
        if not os.path.exists(".identifiant"):
            print(
                '---X Vous devez utiliser "identifiant" au moins une fois avant de pouvoir faire des modifications de code.',
                file=sys.stderr,
            )
            return 1
        with open(".identifiant", "r") as branchFile:
            branch = branchFile.read()
        return branch.strip()

    def wideInput(self, inputMessage=""):
        # Returns either a user input or an argv if their still are some argv left
        if self.cursor < len(sys.argv):
            value = sys.argv[self.cursor]
            print(f"{inputMessage}{value}")
            self.cursor += 1
            return value
        # else...
        return input(inputMessage)

    def editorInput(self, inputMessage="", editorMessage=""):
        # Récupération du texte du rapport
        with open("editor.tmp", "w") as messageTemp:
            messageTemp.write(editorMessage)

        print(inputMessage)
        editor = ""
        if sys.platform == "linux":
            geditExists = run(
                "gedit --version", shell=True, stdout=DEVNULL, stderr=DEVNULL
            )
            if geditExists.returncode == 0:
                editor = "gedit"
            else:
                editor = "nano"
        elif sys.platform == "win32":
            editor = "notepad.exe"
        else:
            print(
                f"---X Votre plateforme {sys.platform} n'est pas supportée.",
                shell=True,
            )
            return 1

        textProcess = run(f"{editor} editor.tmp", shell=True)
        if textProcess.returncode != 0:
            print(
                "---X Une erreur est survenue pendant que vous rentriez votre message, ce dernier n'a pas été récupéré.",
                file=sys.stderr,
            )
            return 1
        # else...
        # Lecture du message enregistré
        with open("editor.tmp", "r") as messageFile:
            return_value = messageFile.read()
        # Suppression du fichier temporaire
        os.remove("editor.tmp")
        return return_value


if __name__ == "__main__":
    richInput = RichInput()
    main(richInput)
