import socket
import sys
import os
import time
import csv

path=os.path.dirname(os.path.realpath(__file__))
client_address = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((client_address,5407))

with open(path+"/exp2_client.csv",'w') as file:
        
        writer = csv.writer(file)
        for _ in range(100):
            writer.writerow([0])          

def write_to_csv(row_number, data):  
     with open(path+"/exp2_client.csv", 'r+', newline='') as file:      
        content = list(csv.reader(file))
        content[row_number - 1] = [data]
        file.seek(0)
        writer = csv.writer(file)
        writer.writerows(content)

while True:
    indata, addr = s.recvfrom(1024)
    print(indata.decode())
    i = indata.decode()[5:]
    t_end=time.time()
    write_to_csv(int(i),t_end)
        
