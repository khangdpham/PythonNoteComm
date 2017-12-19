import mido
print(mido.get_input_names())
with mido.open_input('ARIUS-1 0') as inport:
    for msg in inport:
      if msg.type == 'note_on':
        print(msg)
        
