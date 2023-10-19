import subprocess
import statistics
import math
from time import sleep
import matplotlib.pyplot as plt
import re

time = [num for num in range(1, 101)] # x axis
per_accounts_median = {} # dict of median arrays to represent the different lines (for different number of writing accounts), y axis
delays = {} # dictionary of arrays of delays

for i in range(1, 11):
    print(f'running bash parallel.sh {i}')
    process = subprocess.Popen(['C:/Program Files/Git/bin/bash.exe', 'parallel.sh', str(i)], stdout=subprocess.PIPE, universal_newlines=True)
    accounts_used = i * 10
    print(f"Number of accounts writing to blockchain: {accounts_used}")
    if i not in per_accounts_median:
        per_accounts_median[i] = []
    # parse all lines outputed from the script running the write operations
    for line in iter(process.stdout.readline, ''):
        try:
            # extract numbers from output
            match = re.search(r'\[\d+\] (\d+) (\d+)', line)
            if match:
                number = int(match.group(1))
                time_number = int(match.group(2))
                print(f"t = {time_number} {number} from: '{line.strip()}'")
                for j in range(time_number, 100):
                    if j not in delays:
                        delays[j] = []
                    delays[j].append(number)
            else:
                print(f'error: {line}')

        except ValueError:
            pass  # Skip lines that are not integers

    for k in range(100):
        delays[k].sort()
        mid = math.floor(len(delays[k]) / 2)
        delays_temp = delays[k]
        per_accounts_median[i].append(delays_temp[mid])
        delays[k] = []  # re-initialization of the array for the next stage

    process.wait()

plt.plot(time, per_accounts_median[1], marker='o', label="10")
plt.plot(time, per_accounts_median[2], marker='o', label="20")
plt.plot(time, per_accounts_median[3], marker='o', label="30")
plt.plot(time, per_accounts_median[4], marker='o', label="40")
plt.plot(time, per_accounts_median[5], marker='o', label="50")
plt.plot(time, per_accounts_median[6], marker='o', label="60")
plt.plot(time, per_accounts_median[7], marker='o', label="70")
plt.plot(time, per_accounts_median[8], marker='o', label="80")
plt.plot(time, per_accounts_median[9], marker='o', label="90")
plt.plot(time, per_accounts_median[10], marker='o', label="100")
plt.legend(title='#acc/s writing', bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.xlabel('number of repetition')  # rep of uploading values to blockchain
plt.ylabel('median of delay (ms)')
plt.title('median of delay behavior through time')
plt.show()
