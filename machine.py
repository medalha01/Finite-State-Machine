from states import State


class Machine:
    def __init__(self):
        self.states = []
        self.current_states = list()
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
        if (
            self.get_state(state_identifier).get_transition(symbol)
            != next_state_identifier
        ):
            self.get_state(state_identifier).add_transition(
                symbol, next_state_identifier
            )

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
        transition = []
        for state in self.current_states:
            transition.append(self.get_state(self.state.get_transition(symbol)))
        self.current_states = transition

    def check_transition(self, state_identifier, symbol):
        return self.get_state(state_identifier).get_multiples_transitions(symbol)

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

    def start_machine(self):
        self.current_states.append(self.starting_state)

    def execute_machine(self, input_string):
        self.start_machine()
        for symbol in input_string:
            self.realize_transition(symbol)
        return self.current_state.is_final()

    def check_transition(self, symbol):
        transition = []
        for state in self.current_states:
            if state != None:
                var = state.get_multiples_transitions(symbol)
                print("start")
                if var == None:
                    print("none")
                else:
                    for item in var:
                        print(item)
                        transition.append(self.get_state(item))
                    print("over")
        return transition

    def execute_machine_step(self, symbol):
        transition = []
        for item in self.check_transition(symbol):
            print("Uga")
            print(item.state_identifier)
            transition.append(item)

        return transition

    def set_current_state(self, states):
        self.current_states = states

    def get_alphabet(self):
        return self.alphabet

    def is_final(self):
        for state in self.current_states:
            if state.is_final():
                return True

    def states_to_identifier(self, states):
        auxiliar_state_string = ""
        for state in states:
            if state != None:
                auxiliar_state_string = auxiliar_state_string + state.state_identifier
        return auxiliar_state_string
