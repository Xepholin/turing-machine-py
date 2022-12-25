import ntpath

def print_usage():
    print("\n # USAGE\n"
         " Calcul :\n"
         " python main.py <Path du code> <Entrée> <état initial> <état acceptant>\n")

def print_tape(actual_state, tapes, count_step):
    print("état actuel:", actual_state.name, "/ Step:", count_step, '\n')

    for tape in tapes.values():
        print("ruban:", list(tapes.keys()) [list(tapes.values()).index(tape)] , "tête de lecture:", tape.index)
        print(tape.tape, '\n')

    print("-------------------------------------")

def print_tape5(actual_state, tapes, count_step):
    print("état actuel:", actual_state.name, "/ Step:", count_step, '\n')
    print("            v")

    for tape in tapes.values():
        print([tape.tape[i] for i in range (tape.get_index()-2, tape.get_index()+3)])
            
    print("-------------------------------------")

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def supress_empty(list):
    while '' in list:
        list.remove('')