import subprocess
import statistics
from time import sleep
import matplotlib.pyplot as plt
import re

time = [num for num in range(10)]  # x axis
medians = [0] * 11                 # y axis

for i in range(1, 11):
    process = subprocess.Popen(['C:/Program Files/Git/bin/bash.exe', 'parallel.sh', str(i)], stdout=subprocess.PIPE, universal_newlines=True)
    print("Number of accounts writing: ", i)
    if i not in medians:
        medians[i] = []
    for line in iter(process.stdout.readline, ''):
        try:
            # extract numbers from output
            match = re.search(r'\[\d+\] (\d+) (\d+)', line)
            if match:
                number = int(match.group(1))
                time_number = int(match.group(2))
                print("t = ", time_number)
                medians[time_number] = number
            else:
                print("error")
    
        except ValueError:
            pass  # Skip lines that are not integers

    process.wait()

plt.plot(time, medians,  marker='o', label="1")
plt.plot(time, medians,  marker='o', label="2")
plt.plot(time, medians,  marker='o', label="3")
plt.plot(time, medians,  marker='o', label="4")
plt.plot(time, medians,  marker='o', label="5")
plt.plot(time, medians,  marker='o', label="6")
plt.plot(time, medians,  marker='o', label="7")
plt.plot(time, medians,  marker='o', label="8")
plt.plot(time, medians,  marker='o', label="9")
plt.plot(time, medians,  marker='o', label="10")
plt.legend(title='#acc/s writing', bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.xlabel('number of repetition') # rep of uploading values to blockchain
plt.ylabel('delay (ms)')
plt.title('delay behavior through time')
plt.show()