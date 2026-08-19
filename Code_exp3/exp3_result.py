import csv
import os
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.realpath(__file__))

with open(path+"/exp3_server.csv", 'r') as file1, open(path+"/exp3_client.csv", 'r') as file2, open(path+"/exp3_result.csv", 'w', newline='') as result_file:
    reader1 = csv.reader(file1)
    reader2 = csv.reader(file2)
    writer = csv.writer(result_file)

    row_number = 1 
    for row1, row2 in zip(reader1, reader2):

        if '0' in row2:
            writer.writerow(['loss'])

        else:
            difference = (float(row2[0]) - float(row1[0])) * 1000
            writer.writerow([difference])
            print(f'Hello {row_number} : the latency is {difference} ms')
        
        row_number += 1

data = []
with open(path+"/exp3_result.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        for item in row:
            if item == 'loss':
                data.append(None)  
            else:
                data.append(float(item)) 

x = range(1, 101)
plt.scatter(x, data)

plt.xlabel("Hello i-th")
plt.ylabel("delay (ms)")
plt.savefig(path+"/exp3_result.png")
plt.show()