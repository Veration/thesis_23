import subprocess
import statistics
import math
from time import sleep
import matplotlib.pyplot as plt
import re

time = [num for num in range(1, 101)] # x axis
delays = {} # dictionary of arrays of delays
medians = {} # dict of median arrays to represent the different lines (for different number of writing accounts), y axis
variances = {} # dictionary of arrays of delays
stds = {} # std of arrays of delays
for i in range(1, 11):
    process = subprocess.Popen(['C:/Program Files/Git/bin/bash.exe', 'parallel.sh', str(i)], stdout=subprocess.PIPE, universal_newlines=True)
    print("Number of accounts writing: ", i)
    if i not in medians:
        medians[i] = []
        variances[i] = []
        stds[i] = []
    for line in iter(process.stdout.readline, ''):
        try:
            # extract numbers from output
            match = re.search(r'\[\d+\] (\d+) (\d+)', line)
            if match:
                number = int(match.group(1))
                time_number = int(match.group(2))
                print("t = ", time_number)
                for j in range(time_number, 100):
                    if j not in delays:
                        delays[j] = []
                    delays[j].append(number)

            else:
                print(line)
    
        except ValueError:
            pass  # Skip lines that are not integers

    for k in range(100):
        delays[k].sort()
        variance = statistics.variance(delays[k])
        mid = math.floor(len(delays[k]) / 2)
        delays_temp = delays[k]
        medians[i].append(delays_temp[mid])
        variances[i].append(variance)
        stds[i].append(math.sqrt(variance))
        delays[k] = []  # re-initialization of the array for the next stage 

    process.wait()

plt.plot(time, medians[1],  marker='o', label="10")
plt.plot(time, medians[2],  marker='o', label="20")
plt.plot(time, medians[3],  marker='o', label="30")
plt.plot(time, medians[4],  marker='o', label="40")
plt.plot(time, medians[5],  marker='o', label="50")
plt.plot(time, medians[6],  marker='o', label="60")
plt.plot(time, medians[7],  marker='o', label="70")
plt.plot(time, medians[8],  marker='o', label="80")
plt.plot(time, medians[9],  marker='o', label="90")
plt.plot(time, medians[10], marker='o', label="100")
plt.legend(title='# of sensor nodes', bbox_to_anchor=(1.0, 1.0), loc='upper left')
plt.xlabel('number of repetition') # rep of uploading values to blockchain
plt.ylabel('median of delay (ms)')
plt.title('median of delay behavior through time')
plt.show()

med = [0] * 10
for k in range(1, 11):
    medians[k].sort()
    mid = math.floor(len(medians[k]) / 2)
    med[k - 1] = medians[k][mid]

sensor_number = [num for num in range(1, 11)]
plt.plot(sensor_number, med)
plt.xlabel('number of sensors') # rep of uploading values to blockchain
plt.ylabel('median of delay (ms)')
plt.title('Median of delay in respect to number of sensors')
plt.show()


plt.plot(time, variances[1],  marker='o', label="10")
plt.plot(time, variances[2],  marker='o', label="20")
plt.plot(time, variances[3],  marker='o', label="30")
plt.plot(time, variances[4],  marker='o', label="40")
plt.plot(time, variances[5],  marker='o', label="50")
plt.plot(time, variances[6],  marker='o', label="60")
plt.plot(time, variances[7],  marker='o', label="70")
plt.plot(time, variances[8],  marker='o', label="80")
plt.plot(time, variances[9],  marker='o', label="90")
plt.plot(time, variances[10], marker='o', label="100")
plt.legend(title='# of sensor nodes', bbox_to_anchor=(1.0, 1.0), loc='upper left')
plt.xlabel('execution time (# of readings submitted)') # rep of uploading values to blockchain
plt.ylabel('delay variance to commit (ms^2)')
plt.title('Variance of delay to commit a reading over time of execution')
plt.show()

plt.plot(time, stds[1],  marker='o', label="10")
plt.plot(time, stds[2],  marker='o', label="20")
plt.plot(time, stds[3],  marker='o', label="30")
plt.plot(time, stds[4],  marker='o', label="40")
plt.plot(time, stds[5],  marker='o', label="50")
plt.plot(time, stds[6],  marker='o', label="60")
plt.plot(time, stds[7],  marker='o', label="70")
plt.plot(time, stds[8],  marker='o', label="80")
plt.plot(time, stds[9],  marker='o', label="90")
plt.plot(time, stds[10], marker='o', label="100")
plt.legend(title='# of sensor nodes', bbox_to_anchor=(1.0, 1.0), loc='upper left')
plt.xlabel('execution time (# of readings submitted)') # rep of uploading values to blockchain
plt.ylabel('delay STD to commit (ms)')
plt.title('STD of delay to commit a reading over time of execution')
plt.show()

