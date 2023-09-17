from machine import Machine
from machine_factory import MachineFactory
from states import State


def main():
    machine = MachineFactory.entry_parser("4;A;{D};{a,b};A,a,A;A,a,B;A,b,A;B,b,C;C,b,D")
    print(machine.to_string())
    print(machine.starting_state.state_identifier)
    det_mach = MachineFactory.machine_determination(machine)
    print(det_mach.to_string())


main()
