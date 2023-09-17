from machine import Machine
from states import State
import re


class MachineFactory:
    @staticmethod
    def entry_parser(entry):
        machine = Machine()

        # Split the string by semicolon, but only if it's not inside curly braces
        parameters = re.split(r";(?![^{]*})", entry)

        parameters = [param.strip("{}") for param in parameters]

        machine.set_number_of_states(parameters[0])

        machine.create_state(parameters[1])
        machine.set_starting_state(parameters[1])

        end_states = parameters[2].split(",")

        for state in end_states:
            machine.create_state(state)
            machine.add_end_state(state)

        machine.create_alphabet(parameters[3])
        for transition in parameters[4:]:
            transition_elements = transition.split(",")
            machine.create_state(transition_elements[0])
            machine.create_state(transition_elements[2])
            machine.add_transition(
                transition_elements[0],
                transition_elements[1],
                transition_elements[2],
            )

        return machine

    @staticmethod
    def machine_determizaton(machine):
        new_machine = Machine()
        new_machine.set_number_of_states(machine.number_of_states)

        new_machine.create_state(machine.starting_state.state_identifier)
        new_machine.set_starting_state(machine.starting_state.state_identifier)

        for state in machine.end_states:
            new_machine.create_state(state.state_identifier)
            new_machine.add_end_state(state.state_identifier)

        new_machine.create_alphabet(machine.alphabet)

        for state in machine.states:
            for symbol in machine.alphabet:
                if state.get_transition(symbol) != None:
                    new_machine.create_state(state.get_transition(symbol))
                    new_machine.add_transition(
                        state.state_identifier,
                        symbol,
                        state.get_transition(symbol),
                    )

        return new_machine
