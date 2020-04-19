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
        "Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n---- identifiant\n---- maj\n---- test\n---- fini\n\nVotre demande :\n>> "
    )
    while demande not in [
        "identifiant",
        "maj",
        "test",
        "fini",
        "fusion",
    ]:
        print(
            f"Votre demande {demande} n'a pas été comprise, vous ne pouvez utiliser que l'une des demandes proposées."
        )
        demande = richInput.wideInput(
            "Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n---- identifiant\n---- maj\n---- test\n---- fini\n\nVotre demande :\n>> "
        )

    print()  # A blank line for the style :-)
    if demande == "identifiant":
        identifiant(richInput)
    elif demande == "maj":
        maj(richInput)
    elif demande == "test":
        verifier(richInput)
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
            "L'identifiant que vous avez rentré n'est pas valable, veuillez rentrer un des identifiants possibles."
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
        raise CIException(
            "---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?"
        )
    # else...
    gitProcess = run("git pull origin master", shell=True)
    if gitProcess.returncode != 0:
        raise CIException(
            "---X Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
        )
    # else...
    print("---> Mise à jour effectuée avec succès")


def verifier(richInput):
    listeGroupes = [
        "AI",
        "Animation",
        "Grille",
        "Simulation",
        "SunRise",
        "UI",
    ]
    nomGroupe = richInput.wideInput("Nom du groupe à tester :\n>> ")
    while nomGroupe not in listeGroupes and nomGroupe != "all":
        print(
            "Le nom de groupe que vous avez rentré n'est pas valable, veuillez rentrer un des groupes possibles."
        )
        print("Les groupes possibles sont :\n")
        for groupe in listeGroupes:
            print(f"---- {groupe}")
        print("\n")
        nomGroupe = richInput.wideInput("Nom du groupe à tester :\n>> ")

    if nomGroupe == "all":
        testProcess = run(f"pytest")
    else:
        testProcess = run(f"pytest tests\\test_{nomGroupe}.py")
    print()
    if testProcess.returncode == 1:
        print("---> Certains tests ont échoué")
    elif testProcess.returncode == 0:
        print("---> Les tests ont réussi")
    else:
        raise CIException(
            "---X Une erreur est survenue lors des tests. Demandez de l'aide au groupe DevOps pour régler le problème."
        )


def fini(richInput):
    branch = richInput.user()
    # Récupération du groupe

    # Création d'un message de commit synthétique
    commit = richInput.editorInput(
        "---> Inscrivez votre rapport dans votre éditeur de texte",
        "",
    )
    messageCommit = (
        f"({branch}) {commit}."
    )

    gitProcess = run(f"git checkout {branch}", shell=True)
    if gitProcess.returncode != 0:
        raise CIException(
            "---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?"
        )
    # Ajout de tout le travail fait depuis le dernier commit
    gitProcess = run("git add .", shell=True)
    if gitProcess.returncode != 0:
        raise CIException(
            "---X Le travail que vous avez fait n'a pas pu être ajouté. Demandez de l'aide au groupe DevOps pour régler le problème."
        )

    # Validation du travail effectué
    gitProcess = run(f'git commit -m "{messageCommit}"', shell=True)
    if gitProcess.returncode != 0:
        raise CIException(
            "---X Le travail que vous avez fait n'a pas pu être validé. Demandez de l'aide au groupe DevOps pour régler le problème."
        )
    # Envoi du travail effectué
    gitProcess = run(f"git push", shell=True)
    if gitProcess.returncode != 0:
        raise CIException(
            "---X Le travail que vous avez fait n'a pas pu être enregisté. Demandez de l'aide au groupe DevOps pour régler le problème."
        )
    print("---> Votre travail a bien été enregistré.")


def fusion(richInput):
    nomBranche = richInput.wideInput("Nom de la branche à fusionner :\n>> ")
    gitProcess = run("git checkout master", shell=True)
    if gitProcess.returncode != 0:
        raise CIException(
            "---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?"
        )
    # else...
    gitProcess = run(f"git pull --rebase origin {nomBranche}", shell=True)
    if gitProcess.returncode != 0:
        raise CIException(
            "---X Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
        )
    # else...
    gitProcess = run(f"git push", shell=True)  # Pour mettre à jour le dépôt distant
    if gitProcess.returncode != 0:
        raise CIException(
            "---X Le push de la branche fusionnée a échoué. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
        )
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
            raise CIException(
                '---X Vous devez utiliser "identifiant" au moins une fois avant de pouvoir faire des modifications de code.'
            )
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
            raise CIException(
                f"---X Votre plateforme {sys.platform} n'est pas supportée."
            )

        textProcess = run(f"{editor} editor.tmp", shell=True)
        if textProcess.returncode != 0:
            raise CIException(
                "---X Une erreur est survenue pendant que vous rentriez votre message, ce dernier n'a pas été récupéré."
            )
        # else...
        # Lecture du message enregistré
        with open("editor.tmp", "r") as messageFile:
            return_value = messageFile.read()
        # Suppression du fichier temporaire
        os.remove("editor.tmp")
        return return_value


class CIException(Exception):
    # Special syntax to declare exceptions easily
    pass


if __name__ == "__main__":
    try:
        richInput = RichInput()
        main(richInput)
    except CIException as e:
        print(str(e), file=sys.stderr)
