import socket
import time
import random
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

proxy_address = sys.argv[2]
client_address =sys.argv[4]
timedelay = float(sys.argv[6])
loss_rate= float(sys.argv[8])

s.bind((proxy_address, 5406))


def send(indata,i):
 
    time.sleep(timedelay)
    s.sendto(indata,(client_address,5407))


while True:
    
    indata, addr = s.recvfrom(1024)
    print(indata.decode())
    print('the latency is',timedelay,'s')
    i = int(indata.decode()[5:])
    y = random.choices([0,1], weights=[loss_rate,1-loss_rate])
    print('loss probability is',loss_rate,y)
    if int(y[0]) == 1 :
        threading.Thread(target=send,args=[indata,i]).start()
    
    
    
   
