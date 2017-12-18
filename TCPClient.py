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
  if nt.CurrentNote is not None:
    print(nt.CurrentNote)
  time.sleep(.5)

#try:
#    
#    # Send data
#    message = '1'
#    print(sys.stderr, 'sending "%s"' % message)
#    sock.sendall(message.encode())
#
#    # Look for the response
#    amount_received = 0
#    amount_expected = len(message)
#    
#    while True:
#        data = sock.recv(16)
#        amount_received += len(data)
#        print('received "%s"' % data)
        
        

#finally:
#    print('closing socket')
#    sock.close()