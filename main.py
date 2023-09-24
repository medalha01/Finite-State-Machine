from machine_factory import MachineFactory
from minimizator import MinimizationAlgorithm, MinimizationGroup


def main():
    input_string = str(input())
    machine = MachineFactory.entry_parser(input_string)
    det_mach = MachineFactory.machine_determination(machine)
    machine_string = det_mach.to_string()
    print(machine_string)


def main_mimize():
    input_string = str(input())
    machine = MachineFactory.entry_parser(input_string)
    machine.print_states()
    Minimization = MinimizationAlgorithm(machine)
    mini_machine = Minimization.toMachine()
    print(mini_machine.to_string2())


##main()
main_mimize()
