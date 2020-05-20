#!/usr/bin/python3
import os
import sys
import json
from subprocess import run, DEVNULL


class ContinuousIntegration:
    def __init__(self):
        super(ContinuousIntegration, self).__init__()
        self.cursor = 1
        self.commandes = [
            "identifiant",
            "id",
            "maj",
            "test",
            "fini",
            "fusion",
            "union",
            "final",
            "format",
        ]
        self.commandesPubliques = [
            "identifiant",
            "id",
            "maj",
            "test",
            "fini",
        ]
        self.membres = [
            "alicia",
            "arthur",
            "camille",
            "felipe",
            "litao",
            "lucie",
            "maud",
            "pierre",
            "martin",
            "shao-hen",
            "tbr",
            "theo",
            "thibault",
            "vitor",
        ]
        self.groupes = [
            "AI",
            "Animation",
            "Grille",
            "Simulation",
            "SunRise",
            "UI",
        ]

    def main(self):
        """
        Récupère la commande de l'utilisateur.
        """
        listeCommandesPubliques = ""
        for commandePublique in self.commandesPubliques:
            listeCommandesPubliques += f"---- {commandePublique}\n"
        demande = self.wideInput(
            f"Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n{listeCommandesPubliques}\nVotre demande :\n>> "
        )
        while demande not in self.commandes:
            print(
                f"Votre demande {demande} n'a pas été comprise, vous ne pouvez utiliser que l'une des demandes proposées."
            )
            demande = self.wideInput(
                f"Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n{listeCommandesPubliques}\nVotre demande :\n>> "
            )

        print()  # A blank line for the style :-)
        if demande == "identifiant" or demande == "id":
            self.identifiant()
        elif demande == "maj":
            self.maj()
        elif demande == "test":
            self.verifier()
        elif demande == "fini":
            self.fini()
        elif demande == "fusion":
            self.fusion()
        elif demande == "union":
            self.union()
        elif demande == "format":
            # "Format" est déjà une fonction de la librairie standard
            self.black()

    def identifiant(self):
        """
        Identifie un contributeur en le plaçant sur sa branche.
        """
        listePrenoms = self.membres
        print("Les identifiants possibles sont :\n")
        for prenom in listePrenoms:
            print(f"---- {prenom}")
        print("\n")
        prenomId = self.wideInput("Identifiant :\n>> ")
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
        # checkout sur branche
        gitProcess = self.run(f"git checkout {prenomId}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?"
            )
        print(
            info(
                f"Identification réalisée avec succès, bienvenue {prenomId.capitalize()} :-)"
            )
        )

    def maj(self):
        """
        Réalise un pull depuis le dépot distant.
        """
        branch = self.user()
        gitProcess = self.run(f"git checkout {branch}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?"
            )
        # else...
        gitProcess = self.run(f"git pull origin {branch}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
            )
        # L'étape qui suit n'est plus nécessaire étant donné la façon dont on a écrit union.
        # # else...
        # gitProcess = self.run("git pull origin master", shell=True)
        # if gitProcess.returncode != 0:
        #     raise CIException(
        #         "Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
        #     )
        # else...
        print(info("Mise à jour effectuée avec succès"))

    def verifier(self):
        """
        Lance les unittests grâce à pytest.
        """
        listeGroupes = self.groupes
        nomGroupe = self.wideInput("Nom du groupe à tester :\n>> ")
        while nomGroupe not in listeGroupes and nomGroupe != "all":
            print(
                "Le nom de groupe que vous avez rentré n'est pas valable, veuillez rentrer un des groupes possibles."
            )
            print("Les groupes possibles sont :\n")
            for groupe in listeGroupes:
                print(f"---- {groupe}")
            print("\n")
            nomGroupe = self.wideInput("Nom du groupe à tester :\n>> ")

        if nomGroupe == "all":
            testProcess = self.run(f"pytest", shell=True)
        else:
            testProcess = self.run(
                f"pytest tests/test_{nomGroupe}.py", shell=True
            )
        print()
        if testProcess.returncode == 1:
            print(err("Certains tests ont échoué"))
        elif testProcess.returncode == 0:
            print(info("Les tests ont été passés avec succès"))
        else:
            raise CIException(
                "Une erreur est survenue lors des tests. Demandez de l'aide au groupe DevOps pour régler le problème."
            )

    def fini(self):
        """
        Push les modifications faites sur une branche locale sur la branche du repo distant.
        """
        branch = self.user()
        # Récupération du groupe

        # Création d'un message de commit synthétique
        commit = self.editorInput(
            "Inscrivez votre rapport dans votre éditeur de texte", "",
        )
        messageCommit = f"({branch}) {commit}"

        gitProcess = self.run(f"git checkout {branch}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?"
            )
        # Ajout de tout le travail fait depuis le dernier commit
        gitProcess = self.run("git add .", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "Le travail que vous avez fait n'a pas pu être ajouté. Demandez de l'aide au groupe DevOps pour régler le problème."
            )

        # Validation du travail effectué
        gitProcess = self.run(f'git commit -m "{messageCommit}"', shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "Le travail que vous avez fait n'a pas pu être validé. Demandez de l'aide au groupe DevOps pour régler le problème."
            )
        # Envoi du travail effectué
        gitProcess = self.run(f"git push", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "Le travail que vous avez fait n'a pas pu être enregisté. Demandez de l'aide au groupe DevOps pour régler le problème."
            )
        print(info("Votre travail a bien été enregistré."))

    def fusion(self, branch=None):
        branch = self.wideInput("Nom de la branche à fusionner :\n>> ")
        target = "devops"

        # On passe sur la branche en question
        gitProcess = self.run(f"git checkout {branch}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                f"Vous n'avez pas pu passer sur la branche {branch}."
            )
        # else...
        # On la met à jour par rapport à origin/{branch}. Pas besoin de rebase car origin/branch est forcément en avance.
        gitProcess = self.run(f"git pull origin {branch}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                f"Un conflit semble être apparu lors de la récupération de changements présents sur origin/{branch} mais pas la branche {branch}. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
            )
        # else...
        # On passe sur la branche devops pour y faire la fusion
        gitProcess = self.run(f"git checkout {target}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?"
            )
        # else...
        # On met aussi la branche target à jour par rapport à origin.
        gitProcess = self.run(f"git pull origin {target}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                f"Un conflit semble être apparu lors de la récupération de changements présents sur origin/{target} mais pas la branche {target}. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
            )
        # else...
        # On fusionne les changements de la branche branch visée dans target
        gitProcess = self.run(f"git rebase {branch}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
            )
        # else...
        # Je crois avoir compris comment régler le problème des conflits que j'ai depuis le début du projet. Ajouter un git pull --rebase origin target ici semble tout résoudre.
        gitProcess = self.run(f"git pull --rebase origin {target}", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
            )
        # else...
        # On pousse la nouvelle version de la branche target sur GitHub
        gitProcess = self.run(
            f"git push origin {target}", shell=True
        )  # Pour mettre à jour le dépôt distant
        if gitProcess.returncode != 0:
            raise CIException(
                "Le push de la branche fusionnée a échoué. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
            )
        print(info(f"Fusion de {branch} dans {target} effectuée avec succès"))

    def union(self):
        # Step 0 : Fusionner devops dans master
        # On met master à jour par rapport à ce qui se trouve sur GitHub
        gitProcess = self.run(f"git pull origin master", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "La branche master qui se trouve sur GitHub n'a pas pu être récupérée."
            )
        # else...
        # On fusionne devops dans master
        gitProcess = self.run(f"git pull origin devops", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "Un conflit est apparu lors de la fusion de devops sur master."
            )
        # else...
        # On pousse la nouvelle version de master sur GitHub
        gitProcess = self.run(f"git push origin master", shell=True)
        if gitProcess.returncode != 0:
            raise CIException(
                "La branche master distante n'a pas pu être mise à jour avec le branche master locale."
            )
        # else...
        print()  # Une ligne vide pour le style
        # Step 1 : changer l'id pour prendre celui d'un membre du groupe
        listePrenoms = self.membres
        for branch in listePrenoms:
            # checkout sur branche
            gitProcess = self.run(f"git checkout {branch}", shell=True)
            if gitProcess.returncode != 0:
                raise CIException(
                    f"Vous n'avez pas pu passer sur la branche locale {branch}."
                )
            print(info(f"Vous êtes sur la branche {branch}."))
            # Step 2 : Maj par rapport à origin/branch
            gitProcess = self.run(
                f"git pull --rebase origin {branch}", shell=True
            )
            if gitProcess.returncode != 0:
                raise CIException(
                    f"Vous n'avez pas pu mettre la branche {branch} à jour par rapport à origin/{branch}"
                )
            # else...
            # Step 3 : maj, sortir avec un message d'erreur s'il y a un conflit
            # Dans la mesure où il ne dois pas y avoir de conflits au moment de la fusion du master (qui est toujours en avance par rapport aux autres branches) il faut faire un git pull ici (et pas de rebase).
            gitProcess = self.run("git pull origin master", shell=True)
            if gitProcess.returncode != 0:
                raise CIException(
                    f"Vous n'avez pas pu mettre la branche {branch} à jour par rapport à origin/master"
                )
            # else...
            print(
                info(
                    f"La branche {branch} est à jour par rapport à origin/master"
                )
            )
            # Step 4 : git push
            gitProcess = self.run(f"git push origin {branch}", shell=True)
            if gitProcess.returncode != 0:
                raise CIException(
                    "Un conflit semble être apparu dans l'usage de git. Veuillez prévenir le groupe DevOps pour qu'ils puissent vous aider."
                )
            # else...
            print(
                info(
                    f"La branche origin/{branch} est à jour par rapport à master"
                )
            )
        print(info("Union des branches réalisée avec succès"))

    def black(self):
        """
        Formate les fichiers du répertoire courant suivant les conventions Black.
        """
        argList = []
        for root, dirs, files in os.walk(".", topdown=True):
            for name in files:
                extension = os.path.splitext(name)[-1]
                if extension == ".py":
                    argList.append(os.path.join(root, name))
        self.run(f"black -l 80 {' '.join(argList)}", shell=True)
        print("\n", info("Formatage réalisé avec succès !"))

    def user(self):
        branch = ""
        if not os.path.exists(".identifiant"):
            raise CIException(
                'Vous devez utiliser "identifiant" au moins une fois avant de pouvoir faire des modifications de code.'
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

        print(info(inputMessage))
        editor = ""
        if sys.platform == "linux":
            geditExists = self.run(
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
                f"Votre plateforme {sys.platform} n'est pas supportée."
            )

        textProcess = self.run(f"{editor} editor.tmp", shell=True)
        if textProcess.returncode != 0:
            raise CIException(
                "Une erreur est survenue pendant que vous rentriez votre message, ce dernier n'a pas été récupéré."
            )
        # else...
        # Lecture du message enregistré
        with open("editor.tmp", "r") as messageFile:
            return_value = messageFile.read()
        # Suppression du fichier temporaire
        os.remove("editor.tmp")
        return return_value

    def run(self, commande, *args, **kwargs):
        print(f"\033[93m>> {commande}\033[m")
        return run(commande, *args, **kwargs)


def err(text):
    # Creates a pretty error String from text.
    return f"\033[91m---X {text}\033[m"


def info(text):
    # Ceates a pretty informative String from text
    return f"\033[92m---> {text}\033[m"


class CIException(Exception):
    # Special syntax to declare exceptions easily
    pass


if __name__ == "__main__":
    # On windows, colors will only display correctly in the terminal if a system call has been triggered beforehand. Not that there be a link between the two...
    os.system("")
    try:
        ci = ContinuousIntegration()
        ci.main()
    except CIException as e:
        print(err(str(e)), file=sys.stderr)
    except EOFError as e:
        print("\n", info("Fermeture de ci.py (Ctrl-D)"), sep="")
    except KeyboardInterrupt as e:
        print("\n", err("Interruption de ci.py (Ctrl-C)"), sep="")
