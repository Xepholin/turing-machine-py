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
                        for tape in tapes.values():
                            tape.set_value2index(transition.write[i])
                            
                            if transition.direction[i] == '>':
                                tape.set_index(tape.index + 1)

                                if tape.index == len(tape.tape):
                                    tape.tape.insert(len(tape.tape), '_')

                            elif transition.direction[i] == '<':
                                tape.set_index(tape.index - 1)

                                if tape.index == -1:
                                    tape.tape.insert(0, '_')

                            else:
                                continue

                    return transition.next
        else:
            continue

    print("Reject")
    exit()

def calc_mt(turing, tapes, qinit):
    for state in turing.states:
        if state.name == qinit:
            actual_state = state

    while actual_state != turing.accept:
        for tape in tapes.values():
            print("tête de lecture:", tape.index)
            print(tape.tape, '\n')
        actual_state = one_step(turing, tapes, actual_state)

    return 1