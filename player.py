from tqdm import tqdm
from rich import print
from util import *
import mido
import rich
import rich.live
import rich.table

outport = choose_midi_output_port()
outport.reset()
outport.send(mido.Message('control_change', control=7, value=127))
midfile = mido.MidiFile(choose_midi_file_with_dragdrop())

try:
    for msg in tqdm(midfile.play()):
        if msg.type not in ('note_on', 'note_off', 'pitchwheel'):
             print(msg)
        print(msg)
#        outport.send(normal_to_evy1(msg))
        outport.send(msg)
except KeyboardInterrupt:
    outport.reset()
    outport.close()