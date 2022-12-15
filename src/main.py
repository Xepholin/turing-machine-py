import sys

from utilities import *
from calc import *

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print_usage()
    else:
        turing, tapes = init_all(sys.argv[1], "turing", sys.argv[4], sys.argv[2].lower())

        if calc_mt(turing, tapes, sys.argv[3]):
            print("Accept")
        else:
            print("Reject")