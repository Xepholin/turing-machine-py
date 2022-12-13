import tokenize

from turing import *

def init_tapes(nb):
    return {i: Tape(i,) for i in list(range(nb))}

def text2transitions(path):
    with open(path, 'rb') as f:
        list_transitions = list()
        state_sav = list()
        tape_nbr = 0
        tokens = tokenize.tokenize(f.readline)

        for token in tokens:
            if token.type == 1 or token.type == 54 and token.string != ',':
                state_sav.append(token.string)
                if token.start[0] == 1 and token.start[1] != 0:
                    tape_nbr += 1

            if len(state_sav) == (2 + tape_nbr * 3):
                if len(list_transitions) != 0:
                    for transition in list_transitions:
                        if transition.actual.name == state_sav[0]:
                            actual_state = transition.actual
                            state_sav.pop(0)
                            break
                        elif transition.next.name == state_sav[0]:
                            actual_state = transition.next
                            state_sav.pop(0)
                            break
                        else:
                            actual_state = State(state_sav.pop(0))
                            break
                else:
                    actual_state = State(state_sav.pop(0))

                read = list()
                for i in range (0, tape_nbr):
                    read.append(state_sav.pop(0))

                if len(list_transitions) != 0:
                    for transition in list_transitions:
                        if transition.actual.name == state_sav[0]:
                            next_state = transition.actual
                            state_sav.pop(0)
                            break
                        elif transition.next.name == state_sav[0]:
                            next_state = transition.next
                            state_sav.pop(0)
                            break
                        else:
                            next_state = State(state_sav.pop(0))
                            break
                else:
                    next_state = State(state_sav.pop(0))

                write = list()
                for i in range (0, tape_nbr):
                    write.append(state_sav.pop(0))

                direction = list()
                for i in range (0, tape_nbr):
                    direction.append(state_sav.pop(0))

                new = Transition(actual_state, read, next_state, write, direction)
                
                list_transitions.append(new)
    
    return list_transitions

def extract_states(list_transition):
    list_states = list()

    for transition in list_transition:
        if transition.actual not in list_states:
            list_states.append(transition.actual)
        elif transition.next not in list_states:
            list_states.append(transition.next)
        else:
            continue
    
    return list_states

def fill_states(list_transitions):
    list_states = extract_states(list_transitions)

    for transition in list_transitions:
        for state in list_states:
            if state == transition.actual:
                state.transitions.append(transition)
                break
            else:
                continue

    return list_states