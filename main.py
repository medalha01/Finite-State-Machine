from machine_factory import MachineFactory


def main():
    input_string = str(input())
    machine = MachineFactory.entry_parser(input_string)
    det_mach = MachineFactory.machine_determination(machine)
    machine_string = det_mach.to_string()
    print(machine_string)


main()
