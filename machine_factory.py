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
    def machine_determination(machine: Machine):
        new_machine = Machine()

        transition_tree = list()

        end_states = list()

        machine.start_machine()
        print(machine.current_states[0].state_identifier)

        new_machine.create_state(machine.starting_state.state_identifier)
        new_machine.set_starting_state(machine.starting_state.state_identifier)

        alphabet = machine.get_alphabet()

        for symbol in alphabet:
            list_of_states = machine.execute_machine_step(symbol)

            transition = tuple([machine.current_states, symbol, list_of_states])
            transition_tree.append(transition)

        ##fazer por profundidade se existir uma tupla igual a uma na lista break
        counter = 0
        while True:
            if counter >= len(transition_tree):
                break
            actual_state = transition_tree[counter]
            machine.set_current_state(actual_state[2])
            for symbol in alphabet:
                list_of_states = machine.execute_machine_step(symbol)
                transition = tuple([machine.current_states, symbol, list_of_states])
                print("Check")
                for i in machine.current_states:
                    print(i.state_identifier)
                print(symbol)
                for i in list_of_states:
                    print(i.state_identifier)
                if transition not in transition_tree:
                    transition_tree.append(transition)
            counter += 1

            if counter > 900:
                break

        end_states_identifier = machine.get_end_states_identifiers()

        for transition_and_state in transition_tree:
            primary_state_identifier = new_machine.states_to_identifier(
                transition_and_state[0]
            )
            for i in transition_and_state[0]:
                print(i.state_identifier)
            print("---")
            print(primary_state_identifier)
            secondary_state_identifier = new_machine.states_to_identifier(
                transition_and_state[2]
            )
            if (
                (primary_state_identifier == "")
                or (secondary_state_identifier == "")
                or (symbol == None)
            ):
                continue
            new_machine.create_state(primary_state_identifier)
            for identifier in end_states_identifier:
                if identifier in primary_state_identifier:
                    new_machine.add_end_state(primary_state_identifier)
                    print(primary_state_identifier)
            new_machine.create_state(secondary_state_identifier)
            for identifier in end_states_identifier:
                if identifier in secondary_state_identifier:
                    new_machine.add_end_state(secondary_state_identifier)

            new_machine.add_transition(
                primary_state_identifier,
                transition_and_state[1],
                secondary_state_identifier,
            )

        new_machine.set_number_of_states(len(new_machine.states) - 1)
        new_machine.alphabet = machine.get_alphabet()

        return new_machine
