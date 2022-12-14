import tokenize

from turing import *

# Initialise les rubans avec l'entrée positionner sur le ruban 1
# Retourne un dictionnaire contenant le num du ruban en clé et sa valeur
def init_tapes(nb, input):
    tapes = {i: Tape(i,) for i in list(range(nb))}
    first_tape = tapes.get(0)
    first_tape.set_tape(list(input))
    return tapes

# Importe les données d'un fichier texte pour les transformer en transition
# Puis retourne la liste des transitions et le nb de ruban
# TODO Faire les check pour regarder si les directons sont bien ['>', '<', '-']
def text2transitions(path):
    with open(path, 'rb') as f:
        list_transitions = list()
        state_sav = list()
        tape_nbr = 0
        tokens_list = []
        tokens = tokenize.tokenize(f.readline)

        for token in tokens:
            if token.type in [62, 0]:
                continue
            else:
                # Check si les lignes possèdent bien le bon nombre d'argument, en fonction de la ligne
                if token.start[0] == 1:
                    pass
                else:
                    if token.type in [4, 61] or token.string == ',':
                        pass
                    else:
                        tokens_list.append(token.string)

                    if (token.string == '\n' and token.type == 4) and token.start[1] != 0:
                        if '>' in tokens_list or '<' in tokens_list or '-' in tokens_list:
                            if len(tokens_list) != (1 + tape_nbr * 2):
                                raise ValueError("Le nombre d'argument donnée n'est pas correct, ligne {}".format(token.start[0]))
                        else:
                            if len(tokens_list) != (1 + tape_nbr):
                                raise ValueError("Le nombre d'argument donnée n'est pas correct, ligne {}".format(token.start[0]))
                    
                        tokens_list.clear()


                # Insère les arguments du texte dans la liste state_sav, puis compte le nb de token de la 1ère ligne pour trouver le nb de ruban
                if token.type in [1, 2, 54] and token.string != ',':
                    state_sav.append(token.string)
                    if token.start[0] == 1 and token.start[1] != 0:
                        tape_nbr += 1

                # Créer une nouvelle transition depuis le parsing de state_sav à chaque fois qu'il atteint une certaine longueur en fonction du nb de ruban
                if len(state_sav) == (2 + tape_nbr * 3):
                    if len(list_transitions) != 0:
                        check = False
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
                            actual_state = State(state_sav.pop(0))
                    else:
                        actual_state = State(state_sav.pop(0))

                    read = list()
                    for i in range (0, tape_nbr):
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
                            next_state = State(state_sav.pop(0))
                    elif actual_state.name == state_sav[0]:
                        next_state = actual_state
                        state_sav.pop(0)
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

    return list_transitions, tape_nbr

# Depuis la liste des transitions, trouve les états qui ont été crée
# Retourner la liste des états
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

# Remplit les champs des State avec les données de la liste des transitions
# Retourne la liste des états et le nb de ruban
def init_states(path):
    transitions, tapes_nbr = text2transitions(path)
    list_states = extract_states(transitions)

    for transition in transitions:
        for state in list_states:
            if state == transition.actual:
                state.transitions.append(transition)
                break
            else:
                continue

    return list_states, tapes_nbr

# Initialise une machine de Turing avec les données données en arguments de la méthode
# Retourne la machine de Turing et les rubans
def init_all(path, turing_name, state_accept_name, input):
    if input == "":
        input = ['_']

    states, tapes_nbr = init_states(path)
    alphabet = list(dict.fromkeys((list(input))))
    tapes = init_tapes(tapes_nbr, input)

    for state in states:
        if state.name == state_accept_name:
            accept = state

    turing = Turing(turing_name, alphabet, accept, states)

    return turing, tapes