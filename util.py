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

def phoneme_to_midi_message(phoneme: str):
    char_list = list(phoneme.encode('utf-8'))
    for x in range(len(char_list) - 1):
        char_list.insert(x*2 + 1, 32)
    return mido.Message('sysex', data=[0x43, 0x79, 0x09, 0x00, 0x50, 0x10] + char_list + [0x00])
