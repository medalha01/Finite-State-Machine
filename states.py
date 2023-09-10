class States:
    def __init__(self, state_identifier):
        self.state_identifier = state_identifier
        self.transitions = []
        self.final = False
        self.starting_state = False
        self.dead_state = False

    def add_transition(self, symbol, state_identifier):
        self.transitions.append = (symbol, state_identifier)

    def set_final(self):
        self.final = True

    def set_starting(self):
        self.starting_state = True

    def set_dead(self):
        self.dead_state = True

    def get_transition(self, symbol):
        for transition in self.transitions:
            if transition[0] == symbol:
                return transition[1]
        return "dead"

    def get_transitions(self):
        return self.transitions

    def remove_transition(self, symbol, state_identifier):
        for transition in self.transitions:
            if transition[0] == symbol and transition[1] == state_identifier:
                self.transitions.remove(transition)
                return True
        return False

    def is_final(self):
        return self.final

    def is_dead(self):
        return self.dead_state

    def is_starting(self):
        return self.starting_state
