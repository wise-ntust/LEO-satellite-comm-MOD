import socket
import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = sys.argv[2]
client_address = sys.argv[4]
timedelay=float(sys.argv[6])


s.bind((server_address, 5405))


i = 1
while (i <= 100):
    if i == 101 :
        break
    outdata = 'Hello {}'.format(i)
    s.sendto(outdata.encode(), (client_address,5407))
    print(outdata)
    time.sleep(timedelay)
    print('the latency is',timedelay,'s')
    i += 1

   
