import subprocess
import statistics
import math
from time import sleep
import matplotlib.pyplot as plt
import re

time = [num for num in range(1, 11)] # x axis
medians = [] # array of medians, temporary
medians_dict = {} # dict of median arrays to represent the different lines (for different number of writing accounts)

for i in range(1, 11):
    process = subprocess.Popen(['C:/Program Files/Git/bin/bash.exe', 'parallel.sh', str(i)], stdout=subprocess.PIPE, universal_newlines=True)
    print("Number of accounts writing: ", i)
    if i not in medians_dict:
        medians_dict[i] = []
    for line in iter(process.stdout.readline, ''):
        try:
            # extract numbers from output
            match = re.search(r'\[\d+\] (\d+) (\d+)', line)
            if match:
                number = int(match.group(1))
                time_number = int(match.group(2))
                print("t = ", time_number)
                print("length of medians = ", len(medians))
                if 0 <= time_number < len(medians):
                    medians[time_number] += number
                    
                else:
                    medians.append(number)
                    

                
                medians.sort() # sorting medians
                mid = math.floor(i / 2) # calculate the middle index
                medians_dict[i].append(medians[mid]) # append value of middle index in dictionary
            else:
                print(line)
    
        except ValueError:
            pass  # Skip lines that are not integers

    medians = []   # re-initialization of the array for the next stage

    process.wait()

plt.plot(time, medians_dict[1],  marker='o', label="1")
plt.plot(time, medians_dict[2],  marker='o', label="2")
plt.plot(time, medians_dict[3],  marker='o', label="3")
plt.plot(time, medians_dict[4],  marker='o', label="4")
plt.plot(time, medians_dict[5],  marker='o', label="5")
plt.plot(time, medians_dict[6],  marker='o', label="6")
plt.plot(time, medians_dict[7],  marker='o', label="7")
plt.plot(time, medians_dict[8],  marker='o', label="8")
plt.plot(time, medians_dict[9],  marker='o', label="9")
plt.plot(time, medians_dict[10],  marker='o', label="10")
plt.legend(title='#acc/s writing', bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.xlabel('number of repetition') # rep of uploading values to blockchain
plt.ylabel('median of delay (ms)')
plt.title('median of delay behavior through time')
plt.show()