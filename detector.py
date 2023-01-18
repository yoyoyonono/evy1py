import itertools
from typing import Iterator
import mido
from util import *
import phonemes

input_port: Iterator[mido.Message] = choose_midi_input_port_auto()
output_port = choose_midi_output_port_auto()
output_port.reset()
output_port.send(mido.Message('control_change', channel=0, control=7, value=127))

def pads_to_key(pads: list[bool]):
    try:
        return mapping[tuple(i for i, x in enumerate(pads) if x)]
    except:
        return ''

pads = [False]*8
pad_nums = {36: 0, 38: 1, 42: 2, 46: 3, 49: 4, 45: 5, 41: 6, 51: 7}

mapping = {tuple(): ''}

# generate mapping
phonemes_keys = list(phonemes.phonemes.keys())
choices = list(range(8))
total = 0

for number in range(1, 5):
    for x in itertools.combinations(choices, number):
        if total < len(phonemes_keys):
            mapping[x] = phonemes_keys[total]
            total += 1

print(mapping)

for x in input_port:
    try:
        if x.channel == 9:
            if x.type == 'note_on':
                pads[pad_nums[x.note]] = True
                print(pads, pads_to_key(pads), japanese_to_phoneme(pads_to_key(pads)), sep='\t')
                if japanese_to_phoneme(pads_to_key(pads)):
                    output_port.send(phoneme_to_midi_message(japanese_to_phoneme(pads_to_key(pads))))
            else:
                pads[pad_nums[x.note]] = False
        else:
            if hasattr(x, 'velocity'):
                x.velocity = 127
            output_port.send(x)
    except Exception:
        input_port.close() 
        output_port.close()
        break