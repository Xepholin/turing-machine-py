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

                            if tapes.get(i).index == len(tapes.get(i).tape):
                                tapes.get(i).tape.insert(len(tape.tape), '_')

                        elif transition.direction[i] == '<':
                            tapes.get(i).set_index(tapes.get(i).index - 1)

                            if tapes.get(i).index == -1:
                                tapes.get(i).tape.insert(0, '_')
                                tapes.get(i).set_index(0)

                        else:
                            pass

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
            print("ruban:", list(tapes.keys()) [list(tapes.values()).index(tape)] , "tête de lecture:", tape.index)
            print(tape.tape, '\n')
        

        actual_state = one_step(turing, tapes, actual_state)
        
    return 1