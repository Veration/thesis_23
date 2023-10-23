import subprocess
import statistics
import math
from time import sleep
import matplotlib.pyplot as plt
import re
import statistics

time = [num for num in range(1, 101)] # x axis
per_accounts_median = {} # dict of median arrays to represent the different lines (for different number of writing accounts), y axis
delays = {} # dictionary of arrays of delays
variances = {} # dictionary of arrays of delays

for i in range(1, 11):
    print(f'running bash parallel.sh {i}')
    process = subprocess.Popen(['C:/Program Files/Git/bin/bash.exe', 'parallel.sh', str(i)], stdout=subprocess.PIPE, universal_newlines=True)
    accounts_used = i * 10
    print(f"Number of accounts writing to blockchain: {accounts_used}")
    if i not in per_accounts_median:
        per_accounts_median[i] = []
        variances[i] = []
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
        variance = statistics.variance(delays[k])
        mid = math.floor(len(delays[k]) / 2)
        delays_temp = delays[k]
        per_accounts_median[i].append(delays_temp[mid])
        variances[i].append(variance)
        delays[k] = []  # re-initialization of the array for the next stage

    with open(f"{i*10}.data", "w") as data_file:
        for k in range(0,100):
            data_file.write(f'{per_accounts_median[i][k]}\t{variances[i][k]}\t{math.sqrt(variances[i][k])}\n')
    process.wait()
