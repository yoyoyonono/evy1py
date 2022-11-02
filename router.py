from typing import Iterator
import mido
from util import *

input_port: Iterator[mido.Message] = choose_midi_input_port_auto()
output_port = choose_midi_output_port_auto()
output_port.reset()
channel = int(input('Channel?'))
output_port.send(mido.Message('control_change', channel=channel, control=7, value=127))
if channel == 0: 
    phoneme_list = phoneme_to_midi_message(japanese_to_phoneme(input('Phoneme?'))) # see evy1 midi implementation appendix
    print(phoneme_list, phoneme_list.hex(), sep='\t')
    output_port.send(phoneme_list)

try:
    for x in input_port:
        if x.type != 'clock':
#            if hasattr(x, 'channel'):
#                x.channel = channel
            if hasattr(x, 'velocity'):
                x.velocity = 127
            print(x, x.hex(), sep='\t')
        output_port.send(x)
except KeyboardInterrupt:
    input_port.close()
    output_port.close()