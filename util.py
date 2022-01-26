import mido
import rich.table

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

def normal_to_evy1(message: mido.Message):
    message = message.copy()
    if hasattr(message, 'channel'):
#        msg.velocity = 127
        if message.channel == 8:
            message.channel = 10
        elif message.channel == 15:
            message.channel = 1
        elif message.channel != 9:
            message.channel += 1
    return message

def choose_midi_file_with_dragdrop() -> str:
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    root.update()
    file_path = filedialog.askopenfilename(initialdir='.', title='Select MIDI file', filetypes=(('MIDI files', '*.mid'), ('all files', '*.*')))
    return file_path

def safely_add_message(message: mido.Message, table: rich.table.Table):
    message_type = message.type
    message_channel = str(message.channel) if hasattr(message, 'channel') else 'N/A'
    message_control = str(message.control) if hasattr(message, 'control') else 'N/A'
    message_channel = str(message.channel) if hasattr(message, 'channel') else 'N/A'
    message_note = str(message.note) if hasattr(message, 'note') else 'N/A'
    message_program = str(message.program) if hasattr(message, 'program') else 'N/A'
    message_value = str(message.value) if hasattr(message, 'value') else 'N/A'
    message_velocity = str(message.velocity) if hasattr(message, 'velocity') else 'N/A'
    message_pitch = str(message.pitch) if hasattr(message, 'pitch') else 'N/A'
    message_time = str(message.time) if hasattr(message, 'time') else 'N/A'
    table.add_row(message_type, message_channel, message_control, message_note, message_program, message_value, message_velocity, message_pitch, message_time)