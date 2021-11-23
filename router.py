import mido
from util import *

input_port = choose_midi_input_port()
output_port = choose_midi_output_port()

phonemes = phoneme_to_midi_message(input('Phoneme?')) # see evy1 midi implementation appendix
output_port.send(phonemes)

try:
    for x in input_port:
        if x.type != 'clock':
            print(x)
        output_port.send(x)
except KeyboardInterrupt:
    input_port.close()
    output_port.close()