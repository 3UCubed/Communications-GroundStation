#This is to plot the different points read from the cpp code

import csv
import matplotlib.pyplot as plt

# Read data from CSV file
x = []
y = []
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        if index >= 100:
            break
        x.append(int(row[0]))
        y.append(float(row[1]))

# Generate plot
plt.plot(x, y, marker='o', linestyle='-')
plt.xlabel('Index')
plt.ylabel('Float Value')
plt.title('Float Values vs. Index')
plt.grid(True)
plt.show()
