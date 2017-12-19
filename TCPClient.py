import socket
import sys
from NoteTrainer import NoteTrainer 
from _thread import *
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.0.19', 12345)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)
print(' Starting NoteTrainer')
nt = NoteTrainer()

StopThread= False


def run_note_trainer(note_tr):
  note_tr.main()
  
start_new_thread(run_note_trainer ,(nt,))

while True:
  #try:
    if len(nt.CurrentNote)>0:
      entry = nt.CurrentNote.pop(0)
      str='{}'.format(entry[1])
      print(str)
      sock.sendall(str.encode())
      #data = sock.recv(16)
      #print(data)
    else:
      time.sleep(0.01)
  #except:
  #  continue
  #finally:
  #    print('closing socket')
  #    sock.close()