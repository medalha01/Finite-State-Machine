class MinimizationAlgorithm:
    def __init__(self, machine):
        self.machine = machine
        self.minimization_group = []


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

    def remove(self, state_id):
        for state in self.state_list:
            if state.state_identifier == state_id:
                self.state_list.remove(state)
                return True
        return False
