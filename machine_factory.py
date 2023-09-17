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
    def machine_determizaton(machine: Machine):
        new_machine = Machine()

        transition_tree = list()

        machine.start_machine()

        new_machine.create_state(machine.get_starting_state().state_identifier)
        machine.set_starting_state(machine.get_starting_state().state_identifier)

        alphabet = machine.get_alphabet()

        for symbol in alphabet:
            list_of_states = machine.execute_machine_step(symbol)
            transition = tuple([machine.get_current_state(), symbol, list_of_states])
            transition_tree.append(transition)

        ##fazer por profundidade se existir uma tupla igual a uma na lista break
        counter = 0
        while True:
            actual_state = transition_tree[counter]
            machine.set_current_state(actual_state[2])
            for symbol in alphabet:
                list_of_states = machine.execute_machine_step(symbol)
                transition = tuple(
                    [machine.get_current_state(), symbol, list_of_states]
                )
                if transition not in transition_tree:
                    transition_tree.append(transition)
            counter += 1

            if counter > 50:
                break

        return new_machine
