from util import choose_midi_file_with_dragdrop


with open(choose_midi_file_with_dragdrop(), 'rb') as f:
    array = bytearray(f.read())

if len(array) > 32000:
    array = array[:32000]

out = ''
count = 0
for i in array:
    if count % 16 == 0:
        out += '\n'
    out += '0x{:02x}, '.format(i)
    count += 1
out = out[1:]

with open('out.txt', 'w') as f:
    f.write(out)