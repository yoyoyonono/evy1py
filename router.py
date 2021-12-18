from typing import Iterator
import mido
from util import *

input_port: Iterator[mido.Message] = choose_midi_input_port()
output_port = choose_midi_output_port()

channel = int(input('Channel?'))
if channel == 0: 
    phonemes = phoneme_to_midi_message(input('Phoneme?')) # see evy1 midi implementation appendix
    print(phonemes, phonemes.hex(), sep='\t')
    output_port.send(phonemes)

try:
    for x in input_port:
        if x.type != 'clock':
            x.channel = channel
            if hasattr(x, 'velocity'):
                x.velocity = 127
            print(x, x.hex(), sep='\t')
        output_port.send(x)
except KeyboardInterrupt:
    input_port.close()
    output_port.close()