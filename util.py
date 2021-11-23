import mido

def choose_midi_output_port():
    ports = mido.get_output_names()
    for i, port in enumerate(ports):
        print(f'{i}: {port}')
    port_id = int(input('Choose port: '))
    return mido.open_output(ports[port_id])

def choose_midi_input_port():
    ports = mido.get_input_names()
    for i, port in enumerate(ports):
        print(f'{i}: {port}')
    port_id = int(input('Choose port: '))
    return mido.open_input(ports[port_id])