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
        dead_states = self.__identify_dead()
        self.__remove_states(dead_states)
        self.__minimize()
        self.__destroy_empty_groups()
        self.print_groups()

    def __init_groups(self):
        for state in self.machine.states:
            if state.final is True:
                print("final:", state.state_identifier)
                self.final_states.append(state)
            else:
                print("non_final:", state.state_identifier)
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
                        print("Estado Alcançado:", temp_state.state_identifier)
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

    def __destroy_empty_groups(self):
        for group in self.minimization_group:
            print("GROUPID:", group.group_id)
            print(len(group.state_list))
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
                print("States ID:", state.state_identifier)

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
                        temp_state = list_of_states[0]
                        if temp_state not in state_transition:
                            state_transition.append(temp_state)
            for transtion_state in state_transition:
                if transtion_state.final is True:
                    is_dead = False
            if is_dead is True:
                dead_state.append(state)
                print("State Dead:", state.state_identifier)
        return dead_state

    def __minimize(self):
        aux_minimization_group = []
        counter = 0
        while len(aux_minimization_group) != len(self.minimization_group):
            aux_minimization_group = self.minimization_group.copy()
            for symbol in self.machine.get_alphabet().split(","):
                print("Executing Symbol =>", symbol)
                for group in self.minimization_group:
                    if len(group.state_list) == 0 or group.state_list is None:
                        continue
                    elif len(group.state_list) == 1:
                        continue
                    print("Group =>", group.group_id)
                    new_groups = []
                    for state in group.state_list:
                        print("State =>", state.state_identifier)
                        group_not_found = True
                        self.machine.set_current_state(state)
                        target_state_list = self.machine.execute_machine_step(symbol)
                        if len(target_state_list) == 0 or target_state_list is None:
                            target_state = self.machine.get_state("dead")
                        else:
                            target_state = target_state_list[0]
                        print("Target State =>", target_state.state_identifier)
                        object_target_group = self.get_group_by_id(group.target_group)
                        print("Original Target Group =>", object_target_group.group_id)
                        if target_state not in object_target_group.state_list:
                            group.remove(state.state_identifier)
                            target_id = self.get_new_target(target_state)
                            print("New Target Group =>", target_id)
                            for new_group in new_groups:
                                if new_group.target_group == target_id:
                                    new_group.append(state)
                                    group_not_found = False
                                    break
                            if group_not_found:
                                new_group = MinimizationGroup(
                                    target_id, counter, [state]
                                )
                                new_groups.append(new_group)
                                counter += 1

                    for group_new in new_groups:
                        self.minimization_group.append(group_new)
                    if counter > 900:
                        print("ITS JOEVER")
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
