"""
This module defines the Machine class for managing states.
"""

from states import State


class Machine:
    """
    This class represents a machine for managing states.
    """

    def __init__(self):
        self.states = []
        self.current_states = []
        self.starting_state = None
        self.end_states = []
        self.start_dead_state()
        self.number_of_states = 0
        self.alphabet = ""
        self.epsilon = dict()

    def get_state(self, state_identifier):
        """
        Get the state object with the given state identifier.

        Parameters:
            state_identifier (str): The identifier of the state to retrieve.

        Returns:
            State or None: The State object with the given identifier, or None if not found.
        """
        for state in self.states:
            if state.state_identifier == state_identifier:
                return state
        return None

    def set_number_of_states(self, number):
        """
        Sets the number of states for the object.

        Parameters:
            number (int): The number of states to set.

        Returns:
            None
        """
        self.number_of_states = number

    def start_dead_state(self):
        """
        Initializes the dead state of the object.

        Parameters:
            None

        Returns:
            None
        """
        self.dead_state = State("dead")
        self.dead_state.set_dead()
        self.states.append(self.dead_state)

    def create_state(self, state_identifier):
        """
        Create a new state with the given state identifier.

        Args:
            state_identifier (str): The identifier of the new state.

        Returns:
            None
        """
        if self.get_state(state_identifier) is None:
            self.states.append(State(state_identifier))

    def add_transition(self, state_identifier, symbol, next_state_identifier):
        """
        Adds a transition to the state machine.

        Args:
            state_identifier (str): The identifier of the current state.
            symbol (str): The symbol triggering the transition.
            next_state_identifier (str): The identifier of the next state.

        Returns:
            None
        """
        if (
            self.get_state(state_identifier).get_transition(symbol)
            != next_state_identifier
        ):
            self.get_state(state_identifier).add_transition(
                symbol, next_state_identifier
            )

    def set_starting_state(self, state_identifier):
        """
        Set the starting state of the state machine.

        Params:
            state_identifier (str): The identifier of the state to set as the starting state.

        Returns:
            None
        """
        state = self.get_state(state_identifier)
        state.set_starting()
        self.starting_state = state

    def set_group_as_starting(self, list_of_states):
        self.starting_state = list_of_states

    def add_end_state(self, state_identifier):
        """
        Adds an end state to the state machine.

        Parameters:
            state_identifier (str): The identifier of the state to be added as an end state.

        Returns:
            None
        """
        state = self.get_state(state_identifier)
        state.set_final()
        print(state.state_identifier)
        print(state.final)
        if state not in self.end_states:
            self.end_states.append(state)

    def remove_state(self, state_identifier):
        """
        Removes a state from the list of states.

        Parameters:
            state_identifier (str): The identifier of the state to be removed.

        Returns:
            None
        """
        self.states.remove(self.get_state(state_identifier))

    def remove_transition(self, state_identifier, symbol, next_state_identifier):
        """
        Remove a transition from a state in the finite automaton.

        Args:
            state_identifier (str): The identifier of the state from which to remove the transition.
            symbol (str): The symbol associated with the transition to be removed.
            next_state_identifier (str): The identifier of the next state.

        Returns:
            None

        Raises:
            KeyError: If the state or the transition does not exist.
        """
        return self.get_state(state_identifier).remove_transition(
            symbol, next_state_identifier
        )

    def realize_transition(self, symbol):
        """
        Realizes the transition for the given symbol.

        Parameters:
            symbol (any): The symbol to transition on.

        Returns:
            None
        """
        transition = []
        for state in self.current_states:
            new_state = self.get_state(state.get_transition(symbol))
            if new_state not in transition:
                transition.append(new_state)
        self.current_states = transition
        return transition

    def check_transition_multiples(self, state_identifier, symbol):
        """
        Check if there are multiple transitions for a given state and symbol.

        Args:
            state_identifier (str): The identifier of the state to check.
            symbol (str): The symbol to check for multiple transitions.

        Returns:
            MultiplesTransitions: The multiples transitions for the given state and symbol.
        """
        return self.get_state(state_identifier).get_multiples_transitions(symbol)

    def create_alphabet(self, alphabet):
        """
        Sets the alphabet for the object.

        Parameters:
            alphabet (str): The alphabet to be set.
        """
        self.alphabet = alphabet

    def to_string(self):
        """
        Convert the DFA object to its string representation.

        Returns:
            str: The string representation of the DFA object.
        """
        # Create a list to hold the parts of the string representation
        parts = []

        # Add the number of states as the first parameter
        parts.append(str(self.number_of_states))

        # Add the starting state as the second parameter
        parts.append("{" + self.starting_state.state_identifier + "}")

        # Add the end states as the third parameter
        end_states_str = (
            "{{"
            + "},{".join(state.state_identifier for state in self.end_states)
            + "}}"
        )
        parts.append(end_states_str)

        # Add the alphabet as the fourth parameter
        parts.append("{" + self.alphabet.replace(",&", "") + "}")

        sorted_list = sorted(self.states, key=lambda state: state.state_identifier)

        # Add the transitions as subsequent parameters
        for state in sorted_list:
            elements = state.get_transitions()
            for transition in elements:
                if transition[0] == "&":
                    continue
                transition_string = "{{{}}},{},{{{}}}".format(
                    state.state_identifier,
                    transition[0],  # Input symbol for the transition
                    transition[1],  # Next state for the transition
                )
                parts.append(transition_string)
        # Combine all parts into a single string with semicolons
        return ";".join(parts)

    def start_machine(self):
        """
        Adds the starting state to the list of current states.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        self.current_states.append(self.starting_state)

    def execute_machine(self, input_string):
        """
        Execute the machine with the given input string.

        Parameters:
            input_string (str): The input string to be processed by the machine.

        Returns:
            bool: True if the machine reaches a final state after processing the input string, False otherwise.
        """
        self.start_machine()
        for symbol in input_string:
            self.realize_transition(symbol)
        for state in self.current_states:
            if state.is_final():
                return True
        return False

    def check_transition(self, symbol):
        """
        Check the transition of the given symbol for the current states.

        Parameters:
            symbol (any): The symbol to check the transition for.

        Returns:
            list: A list of states that the symbol transitions to.
        """
        transition = []

        for state in self.current_states:
            if state is None:
                continue

            for letter in state.state_identifier:
                temp = self.get_state(letter)
                if temp is None:
                    continue

                var = temp.get_multiples_transitions(symbol)
                if var is None:
                    continue

                for item in var:
                    list_of_states_epsilon = self.get_epsilon_fecho(item)
                    for states_item in list_of_states_epsilon:
                        if states_item not in transition:
                            transition.append(states_item)

            var = state.get_multiples_transitions(symbol)
            if var is None:
                continue

            for item in var:
                list_of_states_epsilon = self.get_epsilon_fecho(item)
                for states_item in list_of_states_epsilon:
                    if states_item not in transition:
                        transition.append(states_item)

        return transition

    def execute_machine_step(self, symbol):
        """
        Executes a single step of the machine.

        Args:
            symbol: The symbol to be processed.

        Returns:
            transition: A list of transition items.
        """
        transition = []
        for item in self.check_transition(symbol):
            transition.append(item)

        return transition

    def set_current_state(self, states):
        """
        Set the current states of the object.

        Parameters:
            states (list): The list of states to set as the current states.

        Returns:
            None
        """
        self.current_states = []
        try:
            for state in states:
                self.current_states.append(state)
        except TypeError:
            self.current_states.append(states)

    def get_alphabet(self):
        return self.alphabet

    def is_final(self):
        for state in self.current_states:
            if state.is_final():
                return True
        return False

    def states_to_identifier(self, states):
        """
        Generates a string containing the state identifiers of the given list of states.

        Parameters:
            states (list): A list of State objects.

        Returns:
            str: A string containing the state identifiers of the non-null states.
        """
        auxiliar_state_string = ""
        for state in states:
            if state is not None:
                auxiliar_state_string += state.state_identifier
        return auxiliar_state_string

    def get_end_states_identifiers(self):
        """
        Return a list of the identifiers of the end states.

        Returns:
            end_states_identifier (list): A list containing the identifiers of the end states.
        """
        end_states_identifier = []
        for state in self.end_states:
            end_states_identifier.append(state.state_identifier)
        return end_states_identifier

    def build_epsilon(self):
        for state in self.states:
            epsilon_transition = [state]
            auxiliar_state = state
            while True:
                state_epsilon = auxiliar_state.get_transition("&")
                if state_epsilon is None:
                    break
                else:
                    auxiliar_state = self.get_state(state_epsilon)
                    epsilon_transition.append(auxiliar_state)
            self.epsilon[state.state_identifier] = epsilon_transition

    def get_epsilon_fecho(self, state_identifier: str) -> list:
        return self.epsilon.get(state_identifier)
