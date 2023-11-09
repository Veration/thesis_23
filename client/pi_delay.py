import subprocess
import statistics
import math
from time import sleep
import matplotlib.pyplot as plt
import re
import statistics
import numpy as np


numberOfValue = [num for num in range(1, 21)]  # x axis, i-th value uploaded
uploadDelay = []                               # y axis, upload delay

process = subprocess.Popen(["node", "piConnection.js"], stdout=subprocess.PIPE, universal_newlines=True)
for line in iter(process.stdout.readline, ''):
    try:
        # extract numbers from output
        match = re.search(r'(\d+)', line)
        if match:
            delay = int(match.group(1))
            print(f'delay = {delay}')
            uploadDelay.append(delay)
        else:
            print(f'{line}')

    except ValueError:
        pass  # Skip lines that are not integers

process.wait()

# set the number equal to ms of interval in bme680
with open(f"5.data", "w") as data_file: 
    for k in range(0,20):
        data_file.write(f'{uploadDelay[k]}\n')
process.wait()

