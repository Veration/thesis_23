import matplotlib.pyplot as plt
import math
import os
import numpy as np

time = range(1, 21)

files = []
for file in os.listdir("."):
    if file.endswith(".data"):
        files.append(file)

print(files)

indexes = []
# delay
fig, ax = plt.subplots(figsize=(16, 9))

for filename in files:
    i = int(int(filename.replace(".data", "")))
    indexes.append(i)
    if os.path.exists(filename):
        with open(filename, "r") as data_file:
            delay_array = []
            for line in data_file.readlines():
                delay_val = int(line)
                delay_array.append(delay_val)
            plt.plot(time, delay_array, marker='o', label=f"{i}")
ax.legend(title='upload period (ms)', loc='upper right')
plt.xlabel('execution time (# of readings submitted)')
plt.ylabel('delay to commit (ms)')
plt.xticks(np.arange(1, 21, step=1))
plt.show()