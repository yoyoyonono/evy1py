from typing import Iterator
import mido
from util import *

input_port: Iterator[mido.Message] = choose_midi_input_port()
output_port = choose_midi_output_port()
output_port.reset()
channel = int(input('Channel?'))
output_port.send(mido.Message('control_change', channel=channel, control=7, value=127))
if channel == 0: 
    phonemes = phoneme_to_midi_message(input('Phoneme?')) # see evy1 midi implementation appendix
    print(phonemes, phonemes.hex(), sep='\t')
    output_port.send(phonemes)

try:
    for x in input_port:
        if x.type != 'clock':
            if hasattr(x, 'channel'):
                x.channel = channel
            print(x, x.hex(), sep='\t')
        output_port.send(x)
except KeyboardInterrupt:
    input_port.close()
    output_port.close()