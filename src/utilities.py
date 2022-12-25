import tokenize
import ntpath
import re

from turing import *

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

# Initialise les rubans avec l'entrée positionner sur le ruban 1
# Retourne un dictionnaire contenant le num du ruban en clé et sa valeur
def init_tapes(nb, input):
    tapes = {i: Tape(i,) for i in list(range(nb))}
    first_tape = tapes.get(0)

    new_input = list(input)
    new_input.insert(0, '_')
    new_input.insert(0, '_')

    first_tape.set_tape(new_input)
    return tapes

# Importe les données d'un fichier texte pour les transformer en transition
# Puis retourne la liste des transitions et le nb de ruban
# TODO Faire les check pour regarder si les directons sont bien ['>', '<', '-']
def text2transitions(path):
    transition_line = 0
    count_line = 0
    list_transitions = list()
    list_call = list()
    state_sav = list()
    tape_nbr = 0

    states = list()

    with open(path, 'rb') as f:
        lines = f.readlines()
        first_line = re.split(r',|, | |\n|\r', lines[0].decode('utf-8'))

        supress_empty(first_line)
        tape_nbr = len(first_line) - 1

        for line in lines:
            count_line += 1
            tokens = re.split(r',|, | |\n|\r', line.decode('utf-8'))
            supress_empty(tokens)
            if len(tokens) != 0:
                if transition_line%2 == 0:
                    if len(tokens) == (1 + tape_nbr) or len(tokens) == 2:
                        for token in tokens:
                            state_sav.append(token)

                        transition_line += 1
                    else:
                        raise ValueError("Le nombre d'argument donnée n'est pas correct, ligne {}.".format(count_line))
                        
                else:
                    if len(tokens) == (1 + tape_nbr * 2) or len(tokens) == 2:
                        for token in tokens:
                            state_sav.append(token)

                        # Créer une nouvelle transition depuis le parsing de state_sav à chaque fois qu'il atteint une certaine longueur en fonction du nb de ruban
                        if len(tokens) == (1 + tape_nbr * 2):
                            if len(list_transitions) != 0:
                                check = True
                                for transition in list_transitions:
                                    if transition.actual.name == state_sav[0]:
                                        actual_state = transition.actual
                                        state_sav.pop(0)
                                        check = False
                                        break
                                    elif transition.next.name == state_sav[0]:
                                        actual_state = transition.next
                                        state_sav.pop(0)
                                        check = False
                                        break
                                    else:
                                        check = True
                                        continue
                                if check:
                                    check2 = True
                                    for state in states:
                                        if state.name == state_sav[0]:
                                            actual_state = state
                                            state_sav.pop(0)
                                            check2 = False
                                    if check2:
                                        actual_state = State(state_sav.pop(0))
                                        states.append(actual_state)
                            else:
                                actual_state = State(state_sav.pop(0))
                                states.append(actual_state)

                            read = list()
                            for _ in range (tape_nbr):
                                read.append(state_sav.pop(0))

                            if len(list_transitions) != 0:
                                check = True
                                for transition in list_transitions:
                                    if transition.actual.name == state_sav[0]:
                                        next_state = transition.actual
                                        state_sav.pop(0)
                                        check = False
                                        break
                                    elif transition.next.name == state_sav[0]:
                                        next_state = transition.next
                                        state_sav.pop(0)
                                        check = False
                                        break
                                    else:
                                        continue
                                if check:
                                    check2 = True
                                    for state in states:
                                        if state.name == state_sav[0]:
                                            next_state = state
                                            state_sav.pop(0)
                                            check2 = False
                                    if check2:
                                        next_state = State(state_sav.pop(0))
                                        states.append(next_state)
                            elif actual_state.name == state_sav[0]:
                                next_state = actual_state
                                state_sav.pop(0)
                            else:
                                next_state = State(state_sav.pop(0))
                                states.append(next_state)

                            write = list()
                            for _ in range (tape_nbr):
                                write.append(state_sav.pop(0))

                            direction = list()
                            for _ in range (tape_nbr):

                                direction.append(state_sav.pop(0))

                            new = Transition(actual_state, read, next_state, write, direction)
                            list_transitions.append(new)
                        elif len(tokens) == 2:
                            call_stock = []

                            for transition in list_transitions:
                                if transition.actual.name == state_sav[0]:
                                    call_stock.append(transition.actual)
                                    state_sav.pop(0)
                                    break
                                if transition.next.name == state_sav[0]:
                                    call_stock.append(transition.next)
                                    state_sav.pop(0)
                                    break
                            if len(call_stock) != 1:
                                new_state = State(state_sav[0])
                                call_stock.append(new_state)
                                states.append(new_state)
                                state_sav.pop(0)

                            read_call = []
                            for _ in range (tape_nbr):
                                read_call.append(state_sav.pop(0))
                            call_stock.append(read_call)
                            
                            call_stock.append(state_sav.pop(0))

                            for transition in list_transitions:
                                if transition.actual.name == state_sav[0]:
                                    call_stock.append(transition.actual)
                                    state_sav.pop(0)
                                if transition.next.name == state_sav[0]:
                                    call_stock.append(transition.next)
                                    state_sav.pop(0)
                            if len(call_stock) != 1:
                                new_state = State(state_sav[0])
                                call_stock.append(new_state)
                                states.append(new_state)
                                state_sav.pop(0)

                            list_call.append(call_stock.copy())
                            call_stock.clear()
                            
                        transition_line = 0
                    else:
                        raise ValueError("Le nombre d'argument donnée n'est pas correct, ligne {}.".format(count_line))
    return list_transitions, list_call, tape_nbr

# Depuis la liste des transitions, trouve les états qui ont été crée
# Retourner la liste des états
def extract_states(list_transition):
    list_states = list()

    for transition in list_transition:
        if transition.actual not in list_states:
            list_states.append(transition.actual)
        if transition.next not in list_states:
            
            list_states.append(transition.next)
        else:
            continue
    return list_states

# Remplit les champs des State avec les données de la liste des transitions
# Retourne la liste des états et le nb de ruban
def init_states(path):
    transitions, calls, tapes_nbr = text2transitions(path)
    list_states = extract_states(transitions)

    for transition in transitions:
        for state in list_states:
            if state == transition.actual:
                state.transitions.append(transition)
                break
            else:
                continue

    return list_states, calls, tapes_nbr

# Initialise une machine de Turing avec les données données en arguments de la méthode
# Retourne la machine de Turing et les rubans
def init_all(path, input, turing_name, state_init_name, state_accept_name):
    init = None
    accept = None

    if input == "":
        input = ['_']

    states, calls, tapes_nbr = init_states(path)
    alphabet = list(dict.fromkeys((list(input))))
    tapes = init_tapes(tapes_nbr, input)

    for state in states:
        if state.name == state_init_name:
            init = state

        if state.name == state_accept_name:
            accept = state

    if init is None:
        raise ValueError("L'état initial n'a pas été trouvé.")
    elif accept is None:
        raise ValueError("L'état final n'a pas été trouvé.")
    else:
        turing = Turing(turing_name, alphabet, init, accept, states, calls)

        return turing, tapes