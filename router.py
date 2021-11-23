import mido
from util import *

input_port = choose_midi_input_port()
output_port = choose_midi_output_port()

for x in input_port:
    if x.type != 'clock':
        print(x)
    output_port.send(x)

input_port.close()
output_port.close()