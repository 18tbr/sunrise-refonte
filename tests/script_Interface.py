import os
import sys

# Il faut ajouter src au PYTHONPATH avant tout, sinon les modules n'auront pas accès à leurs propres imports.
sys.path.append(f"{os.getcwd()}/src")

from InterfaceGraphique import InterfaceGraphique


def main():
    interface = InterfaceGraphique()
    interface.afficher()

if __name__ == '__main__':
    main()
