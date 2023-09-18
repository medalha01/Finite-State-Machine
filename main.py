from machine_factory import MachineFactory


def main():
    machine = MachineFactory.entry_parser("4;A;{D};{a,b};A,a,A;A,a,B;A,b,A;B,b,C;C,b,D")
    det_mach = MachineFactory.machine_determination(machine)
    for item in det_mach.states:
        print(item.state_identifier)
    print(det_mach.to_string())


main()
