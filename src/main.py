import sys

from utilities import *
from calc import *

if __name__ == "__main__":
    turing, tapes = init_all(sys.argv[1], "turing", sys.argv[4], sys.argv[2])

    if calc_mt(turing, tapes, sys.argv[3]):
        print("Accept")