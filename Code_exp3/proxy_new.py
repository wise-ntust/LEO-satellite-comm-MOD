import socket
import time
import random
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

proxy_address = sys.argv[2]
client_address =sys.argv[4]


s.bind((proxy_address, 5406))


def send(indata,i):
 
    time.sleep(timedelay)
    s.sendto(indata,(client_address,5407))


while True:
    
    indata, addr = s.recvfrom(1024)
    print(indata.decode())
    
    i = int(indata.decode()[5:])

    if 1 <= i <= 65:
        timedelay= 0.1  

    elif 66 <= i <= 83:
        timedelay= 0.3 

    elif 84 <= i <= 92:
        timedelay= 0.5

    elif 93 <= i <= 97:
        timedelay= 0.7
    else:
        timedelay= 0.8
        
    threading.Thread(target=send,args=[indata,i]).start()
    print('the latency is',timedelay*1000,'ms')
    
    
    
    
    
   
