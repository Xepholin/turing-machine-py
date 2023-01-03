import argparse

from init import *
from utilities import *
from calc import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='fonctions', required=True)

    calc_parser = subparsers.add_parser('calc')
    calc_parser.add_argument('entree')
    calc_parser.add_argument('chemin')

    link_parser = subparsers.add_parser('link')
    link_parser.add_argument('entree')
    link_parser.add_argument('chemin_M1')
    link_parser.add_argument('chemin_M2')

    link3_parser = subparsers.add_parser('link3')
    link3_parser.add_argument('entree')
    link3_parser.add_argument('chemin_M1')
    link3_parser.add_argument('chemin_M2')
    link3_parser.add_argument('chemin_M3')

    args = parser.parse_args()

    if args.fonctions == 'calc':
        M1, tapes = init_all(args.chemin, args.entree)
        if calc_mt(M1, tapes):
            print("Accept")
        else:
            print("Reject")

    elif args.fonctions == 'link':
        M1, tapes1 = init_all(args.chemin_M1, args.entree)
        M2, tapes2 = init_all(args.chemin_M2, "")
        
        if len(tapes1) == len(tapes2):
            M3 = link(M1, M2, M1.name, len(tapes1))

            if calc_mt(M3, tapes1):
                print("Accept")
            else:
                print("Reject")
        else:
            raise ValueError("Le nombre de ruban des 2 MT pour le linker est différent.")
    
    elif args.fonctions == 'link3':
        M1, tapes1 = init_all(args.chemin_M1, args.entree)
        M2, tapes2 = init_all(args.chemin_M2, "")
        M3, tapes3 = init_all(args.chemin_M3, "")

        if len(tapes1) == len(tapes2) and len(tapes2) == len(tapes3):
            M4 = link(M2, M3, M2.name, len(tapes1))
            M5 = link(M1, M4, M1.name, len(tapes1))

            if calc_mt(M5, tapes1):
                print("Accept")
            else:
                print("Reject")
                
        else:
            raise ValueError("Le nombre de ruban des 3 MT pour le linker est différent.")