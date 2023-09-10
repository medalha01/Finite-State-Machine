from states import State


class Machine:
    def __init__(self):
        self.states = []
        self.current_state = None
        self.starting_state = None
        self.end_states = []
        self.start_dead_state()
        self.number_of_states = 0
        self.alphabet = ""

    def get_state(self, state_identifier):
        for state in self.states:
            if state.state_identifier == state_identifier:
                return state
        return None

    def set_number_of_states(self, number):
        self.number_of_states = number

    def start_dead_state(self):
        self.dead_state = State("dead")
        self.dead_state.set_dead()
        self.states.append(self.dead_state)

    def create_state(self, state_identifier):
        if self.get_state(state_identifier) == None:
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

    def create_alphabet(self, alphabet):
        self.alphabet = alphabet

    def to_string(self):
        # Create a list to hold the parts of the string representation
        parts = []

        # Add the number of states as the first parameter
        parts.append(str(self.number_of_states))

        # Add the starting state as the second parameter
        parts.append(str(self.starting_state.state_identifier))

        # Add the end states as the third parameter
        for state in self.end_states:
            end_states_str = ",".join(state.state_identifier)

        parts.append("{" + end_states_str + "}")

        parts.append("{" + self.alphabet + "}")

        # Add the transitions as subsequent parameters
        for state in self.states:
            elements = state.get_transitions()

            for transition in elements:
                transition_string = ",".join(
                    [
                        state.state_identifier,
                        transition[0],
                        transition[1],
                    ]
                )
                parts.append(transition_string)

        # Combine all parts into a single string with semicolons
        return ";".join(parts)
