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
    # Récupération du groupe
    groupe = input("Pour quel groupe avez-vous travaillé ?\n>> ")
    while groupe not in ["UI", "AI", "Arduino", "Simulation", "Grille", "SunRise", "Arduino", "DevOps"]:
        print("Le nom de groupe rentré n'est pas reconnu. Les noms de groupe possibles sont : 'UI', 'AI', 'Arduino', 'Simulation', 'Grille', 'SunRise', 'Arduino', et 'DevOps'.", file=sys.stderr)
        groupe = input("Nom du groupe :\n>> ")
    # Récupération de la tâche
    nomTache = input("Sur quelle tâche avez-vous travaillé ?\n>> ")
    cheminTache = f"taches/{groupe}/{nomTache}.json"
    while not os.path.exists(cheminTache):
        print(f"La tâche {nomTache} n'existe pas pour le groupe {groupe}.", file=sys.stderr)
        print(f"Les taches qui existent pour le groupe {groupe} sont :", file=sys.stderr)
        listeTaches = os.listdir(f"taches/{groupe}")
        for tachePossible in listeTaches:
            print(f">> {tachePossible[:-5]}", file=sys.stderr)
        nomTache = input("Sur quelle tâche avez-vous travaillé ?\n>> ")
        cheminTache = f"taches/{groupe}/{nomTache}.json"
    # Lecture du fichier JSON pour voir les valeurs à demander
    with open(cheminTache, 'r') as jsonFile:
        tache = json.load(jsonFile)
    nomTache = tache["nom"]
    if tache["type"] == "general":
        # On a juste besoin d'un rapport, pas de plus que cela
        pass
    elif tache["type"] == "code":
        typeTravail = input(f"Sur quoi avez-vous travaillé pour la tache {nomTache} ? Les valeurs possibles sont :\n>> test\n>> code\n>> revue\nVotre réponse :\n>> ")
        while typeTravail not in ["test", "code", "revue"]:
            print(f"---! La valeur {typeTravail} n'est pas connue.", file=sys.stderr)
            typeTravail = input(f"Sur quoi avez-vous travaillé pour la tache {nomTache} ? Les valeurs possibles sont :\n>> test\n>> code\n>> revue\nVotre réponse :\n>> ")
        if typeTravail == "test":
            tache["etat"] = "test"
        elif typeTravail == "code":
            if tache["etat"] == "incomplet":
                print(f"Vous devez écrire des tests de la fonction {nomTache} avant d'écrire la fonction en elle-même.", file=sys.stderr)
                return 1
            # else...
            tache["etat"] = "code"
        elif typeTravail == "revue":
            if tache["etat"] == "incomplet" or tache["etat"] == "test":
                print("Il faut que vous écriviez la fonction avant de vérifier si elle est correcte.", file=sys.stderr)
                return 1
            # else...
            tache["etat"] = "complet"
        else:
            print("")

    # Récupération du texte du rapport
    with open("message_ci_tmp", 'w') as messageTemp:
        messageTemp.write(tache["rapport"])
        messageTemp.write("---> Inscrivez votre message en dessous\n")

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
    with open("message_ci_tmp", 'r') as messageFile:
        tache["rapport"] = messageFile.read()
    print(tache["rapport"])
    # Suppression du fichier temporaire
    os.remove("message_ci_tmp")
    # Mise à jour du fichier de la tâche
    with open(cheminTache) as tacheFile:
        json.dumps(tache)
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

    # Validation du travail effectué
    tacheRapport = tache["rapport"]
    gitProcess = run(f"git commit -m \"{tacheRapport}\"", shell=True)
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
    data = {}
    # nom de la tâche
    nomTache = input("Nom de la tâche :\n>> ")
    while ascii(nomTache)[1:-1] != nomTache or ' ' in nomTache:
        print("---X Le nom de la tâche n'est pas valide. Il ne doit contenir ni caractère spécial ni espace. Un nom valide est par exemple 'nom_de_tache'.", file=sys.stderr)
        nomTache = input("Nom de la tâche :\n>> ")
    data["nom"] = nomTache
    # nom du groupe
    groupe = input("Nom du groupe :\n>> ")
    while groupe not in ["UI", "AI", "Arduino", "Simulation", "Grille", "SunRise", "Arduino", "DevOps"]:
        print("---X Le nom de groupe rentré n'est pas reconnu. Les noms de groupe possibles sont : 'UI', 'AI', 'Arduino', 'Simulation', 'Grille', 'SunRise', 'Arduino', et 'DevOps'.", file=sys.stderr)
        groupe = input("Nom du groupe :\n>> ")
    data["groupe"] = groupe
    # type de la tâche
    typeTache = input("Type de la tâche :\n>> ")
    while typeTache not in ["general", "code"]:
        print("---X Le type de tâche rentré n'est pas reconnu. Les 2 types de tâches possibles sont 'general' (pour une tâche générale) et 'code' (pour une fonction ou méthode).", file=sys.stderr)
        typeTache = input("Type de la tâche :\n>> ")
    data["type"] = typeTache

    if data["type"] == "general":
        # description
        data["desc"] = input("Description de la tâche :\n>> ")
        # état
        etat = input("Etat de la tâche :\n>> ") or "incomplet"
        while etat not in ["incomplet", "complet"]:
            print("---X L'état rentré n'est pas reconnu. Les états possibles pour une tâche sont 'incomplet' et 'complet'.", file=sys.stderr)
            etat = input("Etat de la tâche :\n>> ") or "incomplet"
        data["etat"] = etat

    else:
        # arguments
        data["arguments"] = input("Description des arguments de la fonction :\n>> ")
        # retour
        data["retour"] = input("Description de ce que la fonction renvoie :\n>> ")
        # description
        data["desc"] = input("Description de la tâche :\n>> ")
        # état
        etat = input("Etat de la tâche :\n>> ") or "incomplet"
        while etat not in ["incomplet", "test", "code", "complet"]:
            print("---X L'état rentré n'est pas reconnu. Les états possibles pour une tâche sont 'incomplet', 'test', 'code', 'revue' et 'complet'.", file=sys.stderr)
            etat = input("Etat de la tâche :\n>> ") or "incomplet"
            data["etat"] = etat

    # rapport
    data["rapport"] = ""

    directory = os.path.join("taches", data["groupe"])
    fileName = os.path.join(directory, "".join([data["nom"], ".json"]))
    with open(fileName, 'w') as tacheFile:
        json.dump(data, tacheFile)
    return 0


def info():
    pass



if __name__ == '__main__':
    fini()
