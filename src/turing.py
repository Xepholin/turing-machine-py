class State(object):
    def __init__(self, name) -> None:
        self.name = name
        self.transitions = []
    
    def __str__(self):
        text = "name: " + self.name + '\n\n'
        for transition in self.transitions:
            text += transition.__str__() + '\n'
        text += "-----------"

        return text

    def get_name(self):
        return self.name

    def get_transition(self):
        return self.transitions

    def set_name(self, name):
        self.name = name
    
    def set_transitions(self, transitions):
        self.transitions = transitions

class Transition(object):
    def __init__(self, actual, read, next, write, direction) -> None:
        self.actual = actual
        self.read = read
        self.next = next
        self.write = write
        self.direction = direction
    
    def __str__(self) -> str:
        return "état actuel: {}\nlecture: {}\nétat suivant: {}\nécriture: {}\ndirection: {}\n".format(self.actual.name, self.read, self.next.name, self.write, self.direction)

    def get_actual(self):
        return self.actual
    
    def get_read(self):
        return self.read

    def get_next(self):
        return self.next
    
    def get_write(self):
        return self.write

    def get_direction(self):
        return self.direction
    
    def set_actual(self, actual):
        self.actual = actual
    
    def set_read(self, read):
        self.read = read

    def set_next(self, next):
        self.next = next
    
    def set_write(self, write):
        self.write = write

    def set_direction(self, direction):
        self.direction = direction

class Turing(object):
    def __init__(self, name, symb, qinit, qaccept, states = [], call = []) -> None:
        self.name = name
        self.symb = symb
        self.init = qinit
        self.accept = qaccept
        self.states = states
        self.call = call

    def get_name(self):
        return self.name
    
    def get_symb(self):
        return self.symb

    def get_accept(self):
        return self.accept

    def get_states(self):
        return self.states

    def get_call(self):
        return self.call

    def set_name(self, name):
        self.name = name

    def set_symb(self, symb):
        self.symb = symb

    def set_accept(self, qaccept):
        self.accept = qaccept

    def set_states(self, states):
        self.states = states
    
    def set_call(self, call):
        self.call = call

class Tape(object):
    def __init__(self, name, index = 2) -> None:
        self.name = name
        self.tape = ['_', '_', '_', '_', '_']   # Initialisation à 5 pour l'affichage
        self.index = index
    
    def get_name(self):
        return self.name

    def get_tape(self):
        return self.tape
    
    def get_index(self):
        return self.index

    def set_name(self, name):
        self.name = name

    def set_tape(self, tape):
        self.tape = tape

    def set_index(self, index):
        self.index = index

    def set_value2index(self, value):
        self.tape[self.index] = value