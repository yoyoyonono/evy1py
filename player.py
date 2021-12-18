import mido
from util import *

midfile = mido.MidiFile('Black_MIDI_Team_-_Bláçk_mïdï.mid')
outport = choose_midi_output_port()
#outport.send(mido.Message('control_change', control=7, value=127))
for msg in midfile.play():
#    print(msg)
    if msg.type == 'note_on' or msg.type == 'note_off':
#        msg.velocity = 127
        if msg.channel == 8:
            msg.channel = 10
        elif msg.channel != 9:
            msg.channel += 1
    outport.send(msg)