from utilities import *
from copy import deepcopy

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
def calc_mt(turing, tapes, qinit):
    count_step = 0

    for state in turing.states:
        if state.name == qinit:
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