import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import mode

# Define the filename
file_path = 'unidirect_120fps.txt'

# Extract the filename from the path
file_name = os.path.splitext(os.path.basename(file_path))[0]

# Read latency values from the text file
latency_values = []
with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            try:
                latency_values.append(float(line))
            except ValueError:
                pass
                
# Fit a normal distribution to the data
mu, std = norm.fit(latency_values)

# Create histogram
plt.hist(latency_values, bins=10, density=True, color='skyblue', edgecolor='black')

# Plot the PDF
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)

# Calculate mode
mode_result = mode(latency_values, keepdims=False)
mode_value = mode_result.mode.item() if mode_result.mode.size == 1 else mode_result.mode[0]

# Add vertical lines for min and max values
min_value = min(latency_values)
max_value = max(latency_values)
plt.axvline(min_value, color='r', linestyle='dashed', linewidth=1, label=f'Min: {min_value:.2f}')
plt.axvline(max_value, color='g', linestyle='dashed', linewidth=1, label=f'Max: {max_value:.2f}')
plt.axvline(mode_value, color='b', linestyle='dashed', linewidth=1, label=f'Mode: {mode_value:.2f}')

# Add labels legend and title
plt.xlabel('Latency (ms)')
plt.ylabel('Density')
plt.title('Distribution of Latency')
plt.legend()

# Show plot
plt.gcf().canvas.set_window_title(file_name)
plt.show()

""" 
# Plot histogram
plt.hist(latency_values, bins=30, density=True, color='skyblue', edgecolor='black')

# Plot normal distribution curve
mu, sigma = np.mean(latency_values), np.std(latency_values)
x = np.linspace(min(latency_values), max(latency_values), 1000)
pdf = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2))
plt.plot(x, pdf, color='k')

plt.xlabel('Latency')
plt.ylabel('Probability Density')
plt.title('Latency Distribution')
plt.show()

"""
