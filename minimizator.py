from machine import Machine
from states import State


class MinimizationAlgorithm:
    def __init__(self, machine: Machine):
        self.machine = machine
        self.minimization_group = []
        self.dead_group = MinimizationGroup("dead", "dead", [])
        self.non_final_states = MinimizationGroup("non_final", "non_final", [])
        self.final_states = MinimizationGroup("final", "final", [])
        self.__init_groups()
        self.__remove_unreachable()
        self.__minimize()
        self.print_groups()

    def __init_groups(self):
        for state in self.machine.states:
            if state.final is True:
                print("final:", state.state_identifier)
                self.final_states.append(state)
            else:
                print("non_final:", state.state_identifier)
                self.non_final_states.append(state)
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
            print(state.state_identifier)
            for symbol in machine_alphabet.split(","):
                list_of_states = self.machine.execute_machine_step(symbol)
                for temp_state in list_of_states:
                    ##temporary_state = self.machine.get_state(identifier)
                    if temp_state not in reacheable_states:
                        print("Estado Alcansado:", temp_state.state_identifier)
                        reacheable_states.append(temp_state)
            counter += 1
        temporary_state = self.machine.get_state("dead")
        if temporary_state not in reacheable_states:
            reacheable_states.append(temporary_state)
        self.__remove_states(reacheable_states)

    def __remove_states(self, state_list):
        for state in self.non_final_states.get_state_list():
            if state not in state_list:
                print("Removido:", state.state_identifier)
                self.non_final_states.remove(state)
        for state in self.final_states.get_state_list():
            if state not in state_list:
                print("Removido Final:", state.state_identifier)
                self.final_states.remove(state)

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
            print(group.group_id)
            for state in group.state_list:
                print(state.state_identifier)

    def __minimize(self):
        new_minimization_group = []
        counter = 0
        for symbol in self.machine.get_alphabet().split(","):
            for group in self.minimization_group:
                new_groups = []
                for state in group.state_list:
                    group_not_found = True
                    self.machine.set_current_state(state)
                    target_state_identifier = self.machine.execute_machine_step(symbol)
                    if target_state_identifier is None:
                        target_state_identifier = "dead"
                    else:
                        target_state = self.machine.get_state(target_state_identifier)
                    print(group.group_id)
                    print(state.state_identifier)
                    print(group.target_group)
                    object_target_group = self.get_group_by_id(group.target_group)
                    if target_state not in object_target_group.state_list:
                        group.remove(state.state_identifier)
                        target_id = self.get_new_target(target_state)
                        for new_group in new_groups:
                            if new_group.target_group == target_id:
                                print(state.state_identifier)
                                new_group.append(state)
                                group_not_found = False
                                break
                        if group_not_found:
                            print(state.state_identifier)
                            new_group = MinimizationGroup(target_id, counter, [state])
                            new_groups.append(new_group)
                            counter += 1
                for group_new in new_groups:
                    self.minimization_group.append(group_new)
                if counter > 30:
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
