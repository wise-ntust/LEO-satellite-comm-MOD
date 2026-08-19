import socket
import sys
import os
import time
import csv

path=os.path.dirname(os.path.realpath(__file__))
server_address = sys.argv[2]
proxy_address = sys.argv[4]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((server_address, 5405))

with open(path+"/exp3_server.csv",'w') as file:
        
        writer = csv.writer(file)
        for i in range(100):
            writer.writerow([])          

def write_to_csv(row_number, data):  
     with open(path+"/exp3_server.csv", 'r+', newline='') as file:      
        content = list(csv.reader(file))
        content[row_number-1] = [data]
        file.seek(0)
        writer = csv.writer(file)
        writer.writerows(content)

i = 1
while (i <= 100):
    if i == 101 :
        break
    outdata = 'Hello {}'.format(i)
    s.sendto(outdata.encode(), (proxy_address,5406))
    t_start=time.time()
    write_to_csv(i,t_start)
    print(outdata)
    i += 1

   
