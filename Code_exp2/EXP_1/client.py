import socket
import sys
    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_address = sys.argv[2]
s.bind((client_address,5407))

while True:
    indata, addr = s.recvfrom(1024)
    print(indata.decode())
    i = indata.decode()[5:]
        