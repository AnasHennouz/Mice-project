import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the filename
file_path = 'vidTestDLC_mobnet_100_miceJun19shuffle1_10000.csv' 

# Extract the filename from the path
file_name = os.path.splitext(os.path.basename(file_path))[0]

# Print first few rows to understand the structure
data = pd.read_csv(file_path)
print(data.head())

# Read likelihood values from the CSV file
likelihood_column = 'DLC_mobnet_100_miceJun19shuffle1_10000.2'
likelihood_values = data[likelihood_column][2:].astype(float).tolist()  

# Create a time vector based on the length of the likelihood values
time = np.arange(len(likelihood_values))

# Plot the likelihood values over time with a more professional look
plt.figure(figsize=(10, 6))  # Set the figure size

# Use a smoother line with larger, more distinct markers
plt.plot(time, likelihood_values, color='#1f77b4', linestyle='-', linewidth=2, marker='o', markersize=4, markerfacecolor='orange', markeredgewidth=1, markeredgecolor='black', label='Likelihood')

# Add labels and title
plt.xlabel('Frame', fontsize=14, fontweight='bold')
plt.ylabel('Likelihood', fontsize=14, fontweight='bold')
plt.title('Evolution of Likelihood over Time', fontsize=16, fontweight='bold')

# Add grid with a specific style
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend with a more professional location
plt.legend(loc='upper right', fontsize=12)

# Set x and y axis limits for better visibility if needed
plt.xlim(0, len(likelihood_values) - 1)
plt.ylim(0, 1)

# Add a background color to the plot area
plt.gca().set_facecolor('#f9f9f9')

# Add a thicker border to the plot
plt.gca().spines['top'].set_linewidth(1.2)
plt.gca().spines['right'].set_linewidth(1.2)
plt.gca().spines['bottom'].set_linewidth(1.2)
plt.gca().spines['left'].set_linewidth(1.2)

# Show plot
plt.gcf().canvas.set_window_title(file_name)
plt.tight_layout()
plt.show()

"""
# Plot the likelihood values over time
plt.plot(time, likelihood_values, color='blue', linestyle='-', marker='o', markersize=2, label='Likelihood')
# Add labels and title
plt.xlabel('Frame')
plt.ylabel('Likelihood')
plt.title('Evolution of Likelihood over Time')
plt.legend()

# Add grid for better readability
plt.grid(True)
"""
