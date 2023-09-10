from states.py import State


class Machine:
    def __init__(self):
        self.states = []
        self.current_state = None
        self.starting_state = None
        self.end_states = []
        self.start_dead_state()

    def get_state(self, state_identifier):
        for state in self.states:
            if state.state_identifier == state_identifier:
                return state
        return None

    def start_dead_state(self):
        self.dead_state = State("dead")
        self.dead_state.set_dead()
        self.states.append(self.dead_state)

    def add_state(self, state_identifier):
        self.states.append(State(state_identifier))

    def add_transition(self, state_identifier, symbol, next_state_identifier):
        self.get_state(state_identifier).add_transition(symbol, next_state_identifier)

    def set_starting_state(self, state_identifier):
        state = self.get_state(state_identifier)
        state.set_starting()
        self.starting_state = state

    def add_end_state(self, state_identifier):
        state = self.get_state(state_identifier)
        state.set_final()
        self.end_states.append(state)

    def remove_state(self, state_identifier):
        self.states.remove(get_state(state_identifier))

    def remove_transition(self, state_identifier, symbol, next_state_identifier):
        return self.get_state(state_identifier).remove_transition(
            symbol, next_state_identifier
        )

    def realize_transition(self, symbol):
        self.current_state = self.get_state(self.current_state.get_transition(symbol))

    def check_transition(self, state_identifier, symbol):
        return self.get_state(state_identifier).get_transition(symbol)
