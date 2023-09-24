from machine import Machine
from states import State


class MinimizationAlgorithm:
    def __init__(self, machine: Machine):
        self.machine = machine
        self.minimization_group = []
        self.dead_group = MinimizationGroup("dead", "dead", [])
        self.non_final_states = MinimizationGroup("non_final", "non_final", [])
        self.final_states = MinimizationGroup("final", "final", [])

        self.dead_states = []
        self.__init_groups()
        self.__remove_unreachable()
        self.__identify_dead()
        for state in self.non_final_states.state_list:
            print("NonFinal:" + state.state_identifier)
        for state in self.final_states.state_list:
            print("Final:" + state.state_identifier)
        self.__minimize()
        self.__destroy_empty_groups()
        ##self.print_groups()

    def __init_groups(self):
        for state in self.machine.states:
            if state.final is True:
                self.final_states.append(state)
            else:
                self.non_final_states.append(state)

        self.non_final_states.remove("dead")
        self.minimization_group.append(self.final_states)
        self.minimization_group.append(self.non_final_states)
        self.dead_group.append(self.machine.get_state("dead"))
        self.minimization_group.append(self.dead_group)

    def __remove_unreachable(self):
        reacheable_states = [self.machine.starting_state]
        machine_alphabet = self.machine.get_alphabet()
        counter = 0
        while counter < len(reacheable_states):
            state = reacheable_states[counter]
            self.machine.set_current_state(state)
            if state is None:
                continue
            for symbol in machine_alphabet.split(","):
                list_of_states = self.machine.execute_machine_step(symbol)
                for temp_state in list_of_states:
                    ##temporary_state = self.machine.get_state(identifier)
                    if temp_state not in reacheable_states:
                        reacheable_states.append(temp_state)
            counter += 1
        temporary_state = self.machine.get_state("dead")
        if temporary_state not in reacheable_states:
            reacheable_states.append(temporary_state)
        self.__remove_states(reacheable_states)

    def __remove_states(self, state_list):
        for state in self.non_final_states.get_state_list():
            if state not in state_list:
                self.non_final_states.remove(state)
        for state in self.final_states.get_state_list():
            if state not in state_list:
                self.final_states.remove(state)

    def __destroy_empty_groups(self):
        for group in self.minimization_group:
            if len(group.state_list) == 0:
                self.minimization_group.remove(group)

    def get_group_by_id(self, group_id):
        for group in self.minimization_group:
            if group.group_id == group_id:
                return group

    def get_new_target(self, state):
        for group in self.minimization_group:
            if state in group.state_list:
                return group.get_group_id()
        return "dead"

    def get_group_by_target(self, target):
        for group in self.minimization_group:
            if target == group.target_group:
                return target
            else:
                return None

    def print_groups(self):
        for group in self.minimization_group:
            print("Group ID:", group.group_id)
            for state in group.state_list:
                print("State:", state.state_identifier)

    def __identify_dead(self):
        dead_state = []
        temp_len = 10
        for state in self.non_final_states.state_list:
            state_transition = [state]
            is_dead = True
            while len(state_transition) != temp_len:
                for state in state_transition:
                    temp_len = len(state_transition)
                    for symbol in self.machine.get_alphabet().split(","):
                        self.machine.set_current_state(state)
                        list_of_states = self.machine.execute_machine_step(symbol)
                        if len(list_of_states) == 0:
                            continue
                        temp_state = list_of_states[0]
                        if temp_state not in state_transition:
                            state_transition.append(temp_state)
            for transtion_state in state_transition:
                if transtion_state.final is True:
                    is_dead = False
            if is_dead is True:
                dead_state.append(state)
        for state in dead_state:
            print("Dead state:", state.state_identifier)
            self.dead_states.append(state.state_identifier)
            self.non_final_states.remove(state.state_identifier)
            self.machine.remove_state(state.state_identifier)

    def toMachine(self):
        machine = Machine()
        machine.set_number_of_states(len(self.minimization_group) - 1)

        machine.create_state(self.machine.starting_state.state_identifier)
        machine.set_starting_state(self.machine.starting_state.state_identifier)
        end_states = []
        valid_states = []
        for group in self.minimization_group:
            if group.state_list[0].final is True:
                machine.create_state(group.state_list[0].state_identifier)
                machine.add_end_state(group.state_list[0].state_identifier)
        for group in self.minimization_group:
            valid_states.append(group.state_list[0])
        machine.create_alphabet(self.machine.get_alphabet())
        transitions = []
        for state in self.machine.states:
            for trans in state.transitions:
                tempo_group = self.get_group_by_id(self.get_new_target(state))
                new_transition_target = self.get_group_by_id(
                    self.get_new_target(self.machine.get_state(trans[1]))
                )

                if new_transition_target.state_list[0].state_identifier == "dead":
                    continue
                if new_transition_target.state_list[0] in valid_states:
                    new_trans = [
                        tempo_group.state_list[0].state_identifier,
                        trans[0],
                        new_transition_target.state_list[0].state_identifier,
                    ]
                    if new_trans not in transitions:
                        transitions.append(new_trans)
        for transi in transitions:
            machine.create_state(transi[0])
            machine.create_state(transi[2])
            machine.add_transition(transi[0], transi[1], transi[2])

        machine.build_epsilon()
        new_start = machine.get_epsilon_fecho(machine.starting_state.state_identifier)
        init_identifier = machine.states_to_identifier(new_start)
        machine.create_state(init_identifier)
        machine.set_starting_state(init_identifier)
        return machine

    def __minimize(self):
        for group in self.minimization_group:
            print("Group ID:", group.group_id)
            for state in group.state_list:
                print("State:", state.state_identifier)
        print("-----------")
        aux_minimization_group = []
        counter = 0
        while len(aux_minimization_group) != len(self.minimization_group):
            aux_minimization_group = self.minimization_group.copy()
            for symbol in self.machine.get_alphabet().split(","):
                symbol_groups = []
                kill_dict = []
                print("Transition Symbol -", symbol)
                for group in self.minimization_group:
                    new_groups = []
                    if len(group.state_list) <= 1 or group.state_list is None:
                        continue
                    for state in group.state_list:
                        print("State Identifier: ", state.state_identifier)
                        group_not_found = True
                        self.machine.set_current_state(state)
                        target_state_list = self.machine.execute_machine_step(symbol)
                        if target_state_list[0].state_identifier in self.dead_states:
                            target_state = self.machine.get_state("dead")
                        elif len(target_state_list) == 0 or target_state_list is None:
                            target_state = self.machine.get_state("dead")
                        else:
                            target_state = target_state_list[0]
                        print("Target State:", target_state.state_identifier)
                        object_target_group = self.get_group_by_id(group.target_group)
                        print("Original Group ID:", group.group_id)
                        print("Original Target", group.target_group)
                        if target_state not in object_target_group.state_list:
                            kill_dict.append = [group, target_state.state_identifier]
                            target_id = self.get_new_target(target_state)
                            print("Where the state is:", target_id)
                            for old_group in new_groups:
                                if old_group.target_group == target_id:
                                    print("Added to Old Group:", old_group.group_id)
                                    print(
                                        "Added to Old Target:", old_group.target_group
                                    )
                                    print("Added State:", state.state_identifier)
                                    old_group.append(state)
                                    group_not_found = False
                            if group_not_found:
                                print("New Group")
                                print("Target ID:", target_id)
                                print("Group ID:", counter)
                                print("Group Member:", state.state_identifier)
                                new_group = MinimizationGroup(
                                    target_id, counter, [state]
                                )
                                new_groups.append(new_group)
                                counter += 1
                    for group_new in new_groups:
                        symbol_groups.append(group_new)
                for group_new in symbol_groups:
                    self.minimization_group.append(group_new)
                for kill_order in kill_dict:
                    kill_order[0].remove(kill_order[1])
                if counter > 900:
                    ##print("ITS JOEVER")
                    break


class MinimizationGroup:
    def __init__(self, target_group, group_id, state_list):
        self.group_id = group_id
        self.target_group = target_group
        self.state_list = state_list

    def append(self, state):
        self.state_list.append(state)
        return self.state_list

    def get_state_list(self):
        return self.state_list

    def get(self, state_id):
        for state in self.state_list:
            if state.state_identifier == state_id:
                return state

    def get_group_id(self):
        return self.group_id

    def set_state_list(self, state_list):
        self.state_list = state_list

    def remove(self, state_id):
        for state in self.state_list:
            if state.state_identifier == state_id:
                self.state_list.remove(state)
                return True
        return False
