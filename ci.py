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
        "Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n---- identifiant\n---- maj\n---- fini\n---- statut\n---- nouveau\n---- info\n\nVotre demande :\n>> "
    )
    while demande not in [
        "identifiant",
        "maj",
        "fini",
        "statut",
        "nouveau",
        "info",
        "groupe",
        "fusion",
    ]:
        print(
            f"Votre demande {demande} n'a pas été comprise, vous ne pouvez utiliser que l'une des demandes proposées."
        )
        demande = richInput.wideInput(
            "Que souhaitez-vous faire ? Vous pouvez répondre avec l'un de :\n>> identifiant\n>> maj\n>> fini\n>> statut\n>> nouveau\n>> info\nVotre demande :\n>> "
        )

    print()  # A blank line for the style :-)
    if demande == "identifiant":
        identifiant(richInput)
    elif demande == "maj":
        maj(richInput)
    elif demande == "fini":
        fini(richInput)
    elif demande == "statut":
        statut(richInput)
    elif demande == "nouveau":
        nouveau(richInput)
    elif demande == "info":
        info(richInput)
    elif demande == "groupe":
        groupe(richInput)
    elif demande == "fusion":
        fusion(richInput)


def identifiant(richInput):
    prenomId = richInput.wideInput("Identifiant :\n>> ")
    with open(".identifiant", "w") as idFile:
        idFile.write(prenomId)
    print("---> Identifiaction réalisée avec succès")


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
    groupe = richInput.wideInput("Pour quel groupe avez-vous travaillé ?\n>> ")
    while groupe not in [
        "UI",
        "AI",
        "Arduino",
        "Simulation",
        "Grille",
        "SunRise",
        "Arduino",
        "DevOps",
    ]:
        print(
            "Le nom de groupe rentré n'est pas reconnu. Les noms de groupe possibles sont :\n---- UI\n---- AI\n---- Arduino\n---- Simulation\n---- Grille\n---- SunRise\n---- Arduino\n---- DevOps",
            file=sys.stderr,
        )
        groupe = richInput.wideInput("Nom du groupe :\n>> ")
    # Récupération de la tâche
    nomTache = richInput.wideInput(
        "Sur quelle tâche avez-vous travaillé ?\n>> "
    )
    cheminTache = f"taches/{groupe}/{nomTache}.json"
    while not os.path.exists(cheminTache):
        print(
            f"La tâche {nomTache} n'existe pas pour le groupe {groupe}.",
            file=sys.stderr,
        )
        print(
            f"Les taches qui existent pour le groupe {groupe} sont :",
            file=sys.stderr,
        )
        listeTaches = os.listdir(f"taches/{groupe}")
        for tachePossible in listeTaches:
            print(f">> {tachePossible[:-5]}", file=sys.stderr)
        nomTache = richInput.wideInput(
            "Sur quelle tâche avez-vous travaillé ?\n>> "
        )
        cheminTache = f"taches/{groupe}/{nomTache}.json"
    # Lecture du fichier JSON pour voir les valeurs à demander
    with open(cheminTache, "r") as jsonFile:
        tache = json.load(jsonFile)
    nomTache = tache["nom"]
    messageEditeur = ""
    if tache["type"] == "general":
        # On a juste besoin d'un rapport, pas de plus que cela
        messageEditeur = (
            "---> Inscrivez votre rapport concernant la tâche en dessous"
        )
        tache["etat"] = "complet"
    elif tache["type"] == "code":
        typeTravail = richInput.wideInput(
            f"Sur quoi avez-vous travaillé pour la tache {nomTache} ? Les valeurs possibles sont :\n>> test\n>> code\n>> revue\nVotre réponse :\n>> "
        )
        while typeTravail not in ["test", "code", "revue"]:
            print(
                f"---! La valeur {typeTravail} n'est pas connue.",
                file=sys.stderr,
            )
            typeTravail = richInput.wideInput(
                f"Sur quoi avez-vous travaillé pour la tache {nomTache} ?\nLes valeurs possibles sont :\n>> test\n>> code\n>> revue\nVotre réponse :\n>> "
            )
        if typeTravail == "test":
            if tache["etat"] == "incomplet":
                tache["etat"] = "test"
            messageEditeur = (
                "---> Inscrivez votre message concernant les tests en dessous"
            )
        elif typeTravail == "code":
            if tache["etat"] == "incomplet":
                print(
                    f"---! Vous devez écrire des tests de la fonction {nomTache} avant d'écrire la fonction en elle-même.",
                    file=sys.stderr,
                )
                return 1
            # else...
            if tache["etat"] == "test":
                tache["etat"] = "code"
            messageEditeur = "---> Inscrivez votre message concernant l'écriture du code en dessous"
        elif typeTravail == "revue":
            if tache["etat"] == "incomplet" or tache["etat"] == "test":
                print(
                    "Il faut que vous écriviez la fonction avant de vérifier si elle est correcte.",
                    file=sys.stderr,
                )
                return 1
            # else...
            if tache["etat"] == "code":
                tache["etat"] = "complet"
            messageEditeur = "---> Inscrivez votre message concernant la revue du code en dessous"

    tacheRapport = tache["rapport"]
    tacheType = tache["type"]
    tache["rapport"] = richInput.editorInput(
        "---> Inscrivez votre phrase de rapport dans votre éditeur de texte",
        f"{tacheRapport}({branch}) {messageEditeur}\n",
    )

    # Mise à jour du fichier de la tâche
    with open(cheminTache, "w") as tacheFile:
        json.dump(tache, tacheFile, sort_keys=True, indent=4)

    # with open(".identifiant", 'r') as branchFile:
    #     branch = branchFile.read();
    # gitProcess = run(f"git checkout {branch}", shell=True)
    # if gitProcess.returncode != 0:
    #     print("---X git n'a pas pu être lancé correctement. Etes-vous certain que git est bien accessible ?", file=sys.stderr)
    #     return 1
    # # Ajout de tout le travail fait depuis le dernier commit
    # gitProcess = run("git add .", shell=True)
    # if gitProcess.returncode != 0:
    #     print("---X Le travail que vous avez fait n'a pas pu être ajouté. Demandez de l'aide au groupe DevOps pour régler le problème.", file=sys.stderr)
    #     return 1
    #
    # # Validation du travail effectué
    # tacheRapport = tache["rapport"]
    # gitProcess = run(f"git commit -m \"{tacheRapport}\"", shell=True)
    # if gitProcess.returncode != 0:
    #     print("---X Le travail que vous avez fait n'a pas pu être validé. Demandez de l'aide au groupe DevOps pour régler le problème.", file=sys.stderr)
    #     return 1
    # # Envoi du travail effectué
    # gitProcess = run(f"git push", shell=True)
    # if gitProcess.returncode != 0:
    #     print("---X Le travail que vous avez fait n'a pas pu être enregisté. Demandez de l'aide au groupe DevOps pour régler le problème.", file=sys.stderr)
    #     return 1
    print("---> Votre travail a bien été enregistré.")


def statut(richInput):
    branch = richInput.user()
    # Récupération du groupe
    groupe = richInput.wideInput(
        "Sur quel groupe voulez avoir un rapport ?\n>> "
    )
    while groupe not in [
        "UI",
        "AI",
        "Arduino",
        "Simulation",
        "Grille",
        "SunRise",
        "Arduino",
        "DevOps",
    ]:
        print(
            "Le nom de groupe rentré n'est pas reconnu. Les noms de groupe possibles sont :\n---- UI\n---- AI\n---- Arduino\n---- Simulation\n---- Grille\n---- SunRise\n---- Arduino\n---- DevOps",
            file=sys.stderr,
        )
        groupe = richInput.wideInput("Nom du groupe :\n>> ")
    listeTaches = os.listdir(f"taches/{groupe}")
    aFinir = []
    for fichierTache in listeTaches:
        with open(f"taches/{groupe}/{fichierTache}", "r") as tacheFile:
            tache = json.load(tacheFile)
            if tache["etat"] == "complet":
                continue
            # else...
            aFinir.append(tache)
    print("\nNom du groupe :", groupe)
    print(f"Total des taches de {groupe} :", len(listeTaches))
    print(f"Taches en cours de {groupe} :", len(aFinir))
    if len(aFinir) > 0:
        print("\nListe des taches à finir :\n")
        for tache in aFinir:
            print("----", tache["nom"], ":", tache["etat"])
    print(f"\n---> Fin du statut de {groupe}")


def groupe(richInput):
    nomGroupe = richInput.wideInput("Nom du groupe à créer :\n>> ")
    nomRepertoire = os.path.join("taches", nomGroupe)
    os.makedirs(nomRepertoire, exist_ok=True)
    print("---> Groupe créé avec succès")


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
    print(f"---> Fusion de {nomBranche} effectuée avec succès")


def nouveau(richInput):
    data = {}
    # nom du groupe
    groupe = richInput.wideInput("Nom du groupe :\n>> ")
    while groupe not in [
        "UI",
        "AI",
        "Arduino",
        "Simulation",
        "Grille",
        "SunRise",
        "Arduino",
        "DevOps",
    ]:
        print(
            "Le nom de groupe rentré n'est pas reconnu. Les noms de groupe possibles sont :\n---- UI\n---- AI\n---- Arduino\n---- Simulation\n---- Grille\n---- SunRise\n---- Arduino\n---- DevOps",
            file=sys.stderr,
        )
        groupe = richInput.wideInput("Nom du groupe :\n>> ")
    data["groupe"] = groupe
    # nom de la tâche
    nomTache = richInput.wideInput("Nom de la tâche :\n>> ")
    while ascii(nomTache)[1:-1] != nomTache or " " in nomTache:
        print(
            "---X Le nom de la tâche n'est pas valide. Il ne doit contenir ni caractère spécial ni espace. Un nom valide est par exemple 'nom_de_tache'.",
            file=sys.stderr,
        )
        nomTache = richInput.wideInput("Nom de la tâche :\n>> ")
    data["nom"] = nomTache
    # type de la tâche
    typeTache = richInput.wideInput("Type de la tâche :\n>> ")
    while typeTache not in ["general", "code"]:
        print(
            "---X Le type de tâche rentré n'est pas reconnu.\nLes 2 types de tâches possibles sont 'general' (pour une tâche générale) et 'code' (pour une fonction ou méthode).",
            file=sys.stderr,
        )
        typeTache = richInput.wideInput("Type de la tâche :\n>> ")
    data["type"] = typeTache

    if data["type"] == "general":
        # description
        data["desc"] = richInput.editorInput(
            "Entrez la description de la tâche dans votre éditeur de texte"
        )
        # état
        etat = richInput.wideInput("Etat de la tâche :\n>> ") or "incomplet"
        while etat not in ["incomplet", "complet"]:
            print(
                "---X L'état rentré n'est pas reconnu.\nLes états possibles pour une tâche sont 'incomplet' et 'complet'.",
                file=sys.stderr,
            )
            etat = input("Etat de la tâche :\n>> ") or "incomplet"
        data["etat"] = etat

    else:
        # arguments
        data["arguments"] = richInput.editorInput(
            "Entrez la description des arguments de la fonction dans votre éditeur de texte"
        )
        # retour
        data["retour"] = richInput.editorInput(
            "Entrez la description de ce que la fonction renvoie dans votre éditeur de texte"
        )
        # description
        data["desc"] = richInput.editorInput(
            "Entrez la description de la tâche dans votre éditeur de texte"
        )
        # état
        etat = richInput.wideInput("Etat de la tâche :\n>> ") or "incomplet"
        while etat not in ["incomplet", "test", "code", "complet"]:
            print(
                "---X L'état rentré n'est pas reconnu. Les états possibles pour une tâche sont 'incomplet', 'test', 'code', 'revue' et 'complet'.",
                file=sys.stderr,
            )
            etat = richInput.wideInput("Etat de la tâche :\n>> ") or "incomplet"

        data["etat"] = etat

    # rapport
    data["rapport"] = ""

    directory = os.path.join("taches", data["groupe"])
    fileName = os.path.join(directory, "".join([data["nom"], ".json"]))
    with open(fileName, "w") as tacheFile:
        json.dump(data, tacheFile, sort_keys=True, indent=4)


def info(richInput):
    # Récupération du groupe
    groupe = richInput.wideInput(
        "Quel est le groupe dont vous chercher une information ?\n>> "
    )
    while groupe not in [
        "UI",
        "AI",
        "Arduino",
        "Simulation",
        "Grille",
        "SunRise",
        "Arduino",
        "DevOps",
    ]:
        print(
            "Le nom de groupe rentré n'est pas reconnu. Les noms de groupe possibles sont :\n---- UI\n---- AI\n---- Arduino\n---- Simulation\n---- Grille\n---- SunRise\n---- Arduino\n---- DevOps",
            file=sys.stderr,
        )
        groupe = richInput.wideInput("Nom du groupe :\n>> ")
    # Récupération de la tâche
    nomTache = richInput.wideInput("Quelle tâche vous intéresse ?\n>> ")
    cheminTache = f"taches/{groupe}/{nomTache}.json"
    while not os.path.exists(cheminTache):
        print(
            f"La tâche {nomTache} n'existe pas pour le groupe {groupe}.",
            file=sys.stderr,
        )
        print(
            f"Les taches qui existent pour le groupe {groupe} sont :",
            file=sys.stderr,
        )
        listeTaches = os.listdir(f"taches/{groupe}")
        for tachePossible in listeTaches:
            print(f">> {tachePossible[:-5]}", file=sys.stderr)
        nomTache = richInput.wideInput("Quelle tâche vous intéresse ?\n>> ")
        cheminTache = f"taches/{groupe}/{nomTache}.json"
    # Lecture du fichier JSON pour voir les valeurs à demander
    with open(cheminTache, "r") as jsonFile:
        tache = json.load(jsonFile)

    print("\nNom de la tâche :", tache["nom"])
    print("Type :", tache["type"])
    print("Groupe assigné :", tache["groupe"])
    print("Avancement :", tache["etat"], "\n")
    if tache["type"] == "general":
        print("Description de la tache :\n", tache["desc"], sep="")
    elif tache["type"] == "code":
        print("Arguments de la fonction :", tache["arguments"])
        print("Retour de la fonction :", tache["retour"])
        print("Description de la fonction :\n", tache["desc"], sep="")
    print("\nRapport de la tache :\n", tache["rapport"], sep="")

    print("---> Fin des informations sur la tache", tache["nom"])


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
