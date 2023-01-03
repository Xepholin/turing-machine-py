import re

from utilities import *
from turing import *

# Initialise les rubans avec l'entrée positionner sur le ruban 1
# Retourne un dictionnaire contenant le num du ruban en clé et sa valeur
def init_tapes(nb, input):
    tapes = {i: Tape(i,) for i in list(range(nb))}
    first_tape = tapes.get(0)

    new_input = list(input)
    new_input.insert(0, '_')
    new_input.insert(0, '_')
    new_input.append('_')
    new_input.append('_')


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

    name = ""
    init = ""
    accept = ""

    states = list()

    with open(path, 'rb') as f:
        lines = f.readlines()
        count = 0   # Le numéro de la ligne quand le code de la MT commence

        for line in lines:
            tokens = re.split(r',|, | ', line.decode('utf-8'))
            supress_empty(tokens)
            if tokens[0] not in ['name:', 'init:', 'accept:', '\n', '\r']:
                break
            else:
                count += 1
            
        first_line = re.split(r',|, | |\n|\r', lines[count].decode('utf-8'))

        supress_empty(first_line)
        tape_nbr = len(first_line) - 1

        for line in lines:
            count_line += 1
            tokens = re.split(r',|, | |\n|\r', line.decode('utf-8'))
            supress_empty(tokens)

            if len(tokens) != 0:
                if tokens[0] == "name:":
                    if len(tokens) >= 2:
                        for i in range(1, len(tokens)):
                            name += tokens[i]
                            name += ' '
                        name = name.strip()
                        continue
                    else:
                        raise ValueError("Le nom est manquant dans le code de la MT")
                    
                if tokens[0] == "init:":
                    if len(tokens) >= 2:
                        for i in range(1, len(tokens)):
                            init += tokens[i]
                            init += ' '
                        init = init.strip()
                        continue
                    else:
                        raise ValueError("Le nom de l'état inital est manquant dans le code de la MT")

                if tokens[0] == "accept:":
                    if len(tokens) >= 2:
                        for i in range(1, len(tokens)):
                            accept += tokens[i]
                            accept += ' '
                        accept = accept.strip()
                        continue
                    else:
                        raise ValueError("Le nom de l'état acceptant est manquant dans le code de la MT")

                # Stock les données des lignes (2 à 2 avant création des objets) dans state_sav + vérification du nombre de données.
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

                        # Créer une nouvelle transition depuis le parsing de state_sav à chaque fois qu'il atteint une certaine longueur en fonction du nb de ruban.
                        if len(tokens) == (1 + tape_nbr * 2):
                            # Partie l'état actuel
                            if len(list_transitions) != 0:
                                check = True
                                # Regarde si l'état existe déjà dans les transitions
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
                                # Si l'état n'existe pas
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

                            # Partie lecture
                            read = list()
                            for _ in range (tape_nbr):
                                read.append(state_sav.pop(0))

                            #Partie état suivant
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

                            # Partie écriture
                            write = list()
                            for _ in range (tape_nbr):
                                write.append(state_sav.pop(0))

                            # Partie direction
                            direction = list()
                            for _ in range (tape_nbr):
                                verif = state_sav.pop(0)
                                
                                if verif in ['<', '>', '-']:
                                    direction.append(verif)
                                else:
                                    raise ValueError("La valeur pour la direction n'est pas valide, ligne {}".format(count_line))

                            new = Transition(actual_state, read, next_state, write, direction)
                            list_transitions.append(new)

                        # Enregistre les informations dans le cas d'un appel à une autre MT, même principe quand pour les transitions
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
                                
                            if len(call_stock) == 0:
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
                                    break
                                if transition.next.name == state_sav[0]:
                                    call_stock.append(transition.next)
                                    state_sav.pop(0)
                                    break

                            if len(call_stock) == 3:
                                new_state = State(state_sav[0])
                                call_stock.append(new_state)
                                states.append(new_state)
                                state_sav.pop(0)

                            list_call.append(call_stock.copy())
                            call_stock.clear()
                            
                        transition_line = 0
                    else:
                        raise ValueError("Le nombre d'argument donnée n'est pas correct, ligne {}.".format(count_line))
            else:
                continue
    
    if not name:
        raise ValueError("Le nom de la MT n'est pas donné")
    if not init:
        raise ValueError("Le nom de l'état inital de la MT n'est pas donné")
    if not accept:
        raise ValueError("Le nom de l'état acceptant de la MT n'est pas donné")

    return list_transitions, list_call, tape_nbr, name, init, accept

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
    transitions, calls, tapes_nbr, name, init, accept = text2transitions(path)
    list_states = extract_states(transitions)

    for transition in transitions:
        for state in list_states:
            if state == transition.actual:
                state.transitions.append(transition)
                break
            else:
                continue

    return list_states, calls, tapes_nbr, name, init, accept

# Initialise une machine de Turing avec les données données en arguments de la méthode
# Retourne la machine de Turing et les rubans
def init_all(path, input):
    if input == "":
        input = ['_']

    states, calls, tapes_nbr, name, init, accept = init_states(path)
    alphabet = list(dict.fromkeys((list(input))))
    tapes = init_tapes(tapes_nbr, input)

    for state in states:
        if state.name == init:
            stateInit = state

        if state.name == accept:
            stateAccept = state

    if init is None:
        raise ValueError("L'état initial n'a pas été trouvé.")
    elif accept is None:
        raise ValueError("L'état final n'a pas été trouvé.")
    else:
        turing = Turing(name, alphabet, stateInit, stateAccept, states, calls)

        return turing, tapes