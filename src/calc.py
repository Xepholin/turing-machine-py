from copy import deepcopy

from turing import *
from utilities import *
from init import *

# Effectue 1 pas de calcul en utilisant les arguments donnés
# Retourne l'état suivant si les valeur de lecture de l'état actuel a bien été trouvé puis que le ruban a bien été modifié
# Sinon renvoie 0
def one_step(turing, tapes, actual_state):
    read = []

    for i in range (0, len(tapes)):
        tape = tapes.get(i)
        read.append(tape.tape[tape.index])

    for state in turing.states:
        if state == actual_state:
            for transition in state.transitions:
                if transition.read == read:
                    for i in range (0, len(tapes)):
                        tapes.get(i).set_value2index(transition.write[i])
                        
                        if transition.direction[i] == '>':
                            tapes.get(i).set_index(tapes.get(i).index + 1)

                            # Ajout de blancs s'il n'y en a plus assez (inclut l'affichage)
                            if tapes.get(i).index == len(tapes.get(i).tape) - 2:
                                tapes.get(i).tape.insert(len(tapes.get(i).tape), '_')
                                tapes.get(i).tape.insert(len(tapes.get(i).tape) + 1, '_')

                        elif transition.direction[i] == '<':
                            tapes.get(i).set_index(tapes.get(i).index - 1)

                            # Ajout de blancs s'il n'y en a plus assez (inclut l'affichage)
                            if tapes.get(i).index == 1:
                                tapes.get(i).tape.insert(0, '_')
                                tapes.get(i).set_index(2)

                        else:
                            pass
                    return transition.next
        else:
            continue
    return 0

# Calcul la machine de Turing tant que l'état actuel n'est pas l'état acceptant
# Renvoie 1 si l'état acceptant est atteint, sinon 0
def calc_mt(turing, tapes):
    count_step = 0

    for state in turing.states:
        if state == turing.init:
            actual_state = state
            temp_state = actual_state
    
    print_tape5(actual_state, tapes, count_step)

    while actual_state != turing.accept:
        actual_state = one_step(turing, tapes, actual_state)
        count_step += 1
        if actual_state:
            temp_state = actual_state
            print_tape5(actual_state, tapes, count_step)
            
        else:
            print_tape5(temp_state, tapes, count_step)
            return 0
        
    return 1

# Créer une nouvelle MT fait à partir de la M1, qui dans son code, appelle M2
# Renvoie la nouvelle MT
def link(M1, M2, name, tape_nbr):
    M1_copy = deepcopy(M1)
    M2_copy = deepcopy(M2)

    # Le read et le write pour les transitions entre les 2 MT
    direction = []
    for _ in range (tape_nbr):
        direction.append('-')

    for state in M2_copy.states:
        state.set_name(state.name + M2_copy.name)

    for call in M1_copy.call:
        actual_state, read, M2_name, next_state = call

        if M2_name == M2_copy.name:

            for state in M1_copy.states:
                if state.name == actual_state.name:
                    state.transitions.append(Transition(state, read, M2_copy.init, read, direction))

            for state in M2_copy.states:
                if state not in M1_copy.states:
                    M1_copy.states.append(state)
                else:
                    continue

            for state in M1_copy.states:
                for transition in state.transitions:
                    if transition.next.name == M2_copy.accept.name:
                        if len(transition.next.transitions) == 0:
                            transition.next.transitions.append(Transition(transition.next, transition.write, next_state, transition.write, direction))
                        else:
                            # Evite d'avoir 2 fois les mêmes transitions depuis "l'état acceptant" M2 dans M1
                            check = True

                            for transition_accept in transition.next.transitions:
                                if transition_accept.read == read and transition_accept.next == next_state:
                                    check = False
                                    break
                            if check:
                                transition.next.transitions.append(Transition(transition.next, transition.write, next_state, transition.write, direction))
                    else:
                        continue
        else:
            raise ValueError("Le nom donné à la transition ne correspond pas au nom de la 2e MT.")

    M1_copy.set_name(name)

    return M1_copy