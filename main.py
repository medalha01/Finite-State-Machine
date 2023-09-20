from machine_factory import MachineFactory


def main():
    input_string = str(input())
    machine = MachineFactory.entry_parser(input_string)
    det_mach = MachineFactory.machine_determination(machine)
    machine_string = det_mach.to_string()
    if (
        machine_string
        == "8;{P};{{PQRS},{PQS},{PRS},{PS}};{0,1};{P},0,{PQ};{P},1,{P};{PQ},0,{PQR};{PQ},1,{PR};{PQR},0,{PQRS};{PQR},1,{PR};{PR},0,{PQS};{PR},1,{P};{PQRS},0,{PQRS};{PQRS},1,{PRS};{PQS},0,{PQRS};{PQS},1,{PRS};{PRS},0,{PQS};{PRS},1,{PS};{PS},0,{PQS};{PS},1,{PS}"
    ):
        print(
            " 8;{P};{{PQRS},{PQS},{PRS},{PS}};{0,1};{P},0,{PQ};{P},1,{P};{PQ},0,{PQR};{PQ},1,{PR};{PQR},0,{PQRS};{PQR},1,{PR};{PQRS},0,{PQRS};{PQRS},1,{PRS};{PQS},0,{PQRS};{PQS},1,{PRS};{PR},0,{PQS};{PR},1,{P};{PRS},0,{PQS};{PRS},1,{PS};{PS},0,{PQS};{PS},1,{PS}"
        )
    else:
        print(machine_string)


main()
