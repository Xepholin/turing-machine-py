import argparse

from utilities import *
from calc import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='fonctions', required=True)

    calc_parser = subparsers.add_parser('calc')
    calc_parser.add_argument('entree')
    calc_parser.add_argument('chemin')
    calc_parser.add_argument('etat_initial')
    calc_parser.add_argument('etat_acceptant')

    link_parser = subparsers.add_parser('link')
    link_parser.add_argument('entree')
    link_parser.add_argument('chemin_M1')
    link_parser.add_argument('etat_initial_M1')
    link_parser.add_argument('etat_acceptant_M1')
    link_parser.add_argument('chemin_M2')
    link_parser.add_argument('etat_initial_M2')
    link_parser.add_argument('etat_acceptant_M2')

    args = parser.parse_args()

    if args.fonctions == 'calc':
        M1, tapes = init_all(args.chemin, args.entree, path_leaf(args.chemin), args.etat_initial, args.etat_acceptant)

        if calc_mt(M1, tapes, args.etat_initial):
            print("Accept")
        else:
            print("Reject")

    elif args.fonctions == 'link': 
        M1, tapes = init_all(args.chemin_M1, args.entree, path_leaf(args.chemin_M1), args.etat_initial_M1, args.etat_acceptant_M1)
        M2, _ = init_all(args.chemin_M2, args.entree, path_leaf(args.chemin_M2), args.etat_initial_M2, args.etat_acceptant_M2)
        
        M3 = linker(M1, M2, "M3")

        if calc_mt(M3, tapes, args.etat_initial_M1):
            print("Accept")
        else:
            print("Reject")
            