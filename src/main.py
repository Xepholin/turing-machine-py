from utilities import *

list_transitions = text2transitions("test")
list_states = fill_states(list_transitions)

tapes = init_tapes(2)

for tape in tapes.values():
    print(tape.tape)

for state in list_states:
    print(state)