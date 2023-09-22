from machine import Machine


class MinimizationAlgorithm:
    def __init__(self, machine: Machine):
        self.machine = machine
        self.minimization_group = []
        self.dead_group = MinimizationGroup(None, "dead", [])
        self.non_final_states = MinimizationGroup("non_final", "non_final", [])
        self.final_states = MinimizationGroup("final", "final", [])
        self.__init_groups()
        self.__remove_unreachable()

    def __init_groups(self):
        for state in self.machine.states:
            if state.is_final:
                self.final_states.append(state)
            else:
                self.non_final_states.append(state)
        self.minimization_group.append(self.final_states)
        self.minimization_group.append(self.non_final_states)
        self.minimization_group.append(self.dead_group)

    def __remove_unreachable(self):
        reacheable_states = [self.machine.starting_state]
        machine_alphabet = self.machine.get_alphabet()
        for state in reacheable_states:
            self.machine.set_current_state(state)
            for symbol in machine_alphabet:
                list_of_states = self.machine.execute_machine_step(symbol)
                for identifier in list_of_states:
                    temporary_state = self.machine.get_state(identifier)
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
