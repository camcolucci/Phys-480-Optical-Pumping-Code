import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import false
import os

directory = '4_18_24-OP/'

# List to store results for each file
all_results = {}

# Loop through each file in the directory
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
        
    df = pd.read_csv(filepath, header=None)
    # Load the CSV file

    df.columns = ['time', 'field_voltage', 'absorption_voltage']

    # Calculate the differences between consecutive absorption_voltage readings
    df['voltage_difference'] = df['absorption_voltage'].diff()

    # We want to find significant negative changes, indicating downward spikes
    # You might need to adjust the threshold according to your specific data characteristics
    spike_indices = []

    # Loop through the DataFrame to find sequences that meet the criteria
    # for i in range(1, len(df)):
    #     # Check if the initial drop is greater than -4
    #     if df.loc[i, 'absorption_voltage'] < -4:
    #         # Continue to check for consecutive negative deltas
    found = False
    spikes = []

    for j in range(1, len(df)):
        if df.loc[j, 'absorption_voltage'] < -4:
            if df.loc[j, 'voltage_difference'] > 0 and not found:
                # The point just before this positive change is the spike
                spikes.append((j-1, df.loc[j - 1, 'absorption_voltage'], df.loc[j - 1, 'field_voltage']))
                # spike_indices.append(j - 1)
                # field_voltages_at_spikes.append(df.loc[j - 1, 'field_voltage'])
                found = True
        try:
            if df.loc[j, 'absorption_voltage'] - df.loc[j+50, 'absorption_voltage'] > 0:
                found = False
        except:
            pass

    print(spikes)

    # Convert to a NumPy array for possible further operations

    if spikes:
        min_spike = min(spikes, key=lambda x: x[1])
        min_index = spikes.index(min_spike)

        # Determine the index range for the two spikes before and after the minimum spike
        start = max(0, min_index - 2)
        end = min(len(spikes), min_index + 3)
        
        # Extract the required spike data
        relevant_spikes = spikes[start:end]

        # Calculate adjusted absorption voltages based on the central spike's absorption voltage
        central_absorption_voltage = min_spike[2]
        voltage_difs = [spike[2] - central_absorption_voltage for spike in relevant_spikes]
        b_difs = [voltage*8.991*10**-3*11/0.1639 for voltage in voltage_difs]
        # Store results using the numeric prefix
        numeric_prefix = filename.split('k')[0]  # Splits and takes the part before the first '4'
        numeric_prefix = int(numeric_prefix) 
        all_results[numeric_prefix] = b_difs

    
    # print("Adjusted Spike Data:", voltage_difs)

print(all_results)
# Prepare data for plotting
x = []  # Numeric prefixes
y = []  # b values
slopes = []  # Slopes between successive spikes
colors = ['red', 'green', 'blue', 'orange', 'purple']  # colors for spikes 1-5

# Populate x, y for scatter plot and slopes
for numeric_prefix, b_vals in all_results.items():
    for i, b_val in enumerate(b_vals):
        if i < 5:  # Only consider the first five spikes if there are more
            x.append(numeric_prefix)
            y.append(b_val)
            if i > 0:  # Calculate slope if not the first spike
                slope = (b_vals[i] - b_vals[i-1]) / 1  # Assuming uniform distance of 1 between spikes
                slopes.append((numeric_prefix, slope))

# Create the first scatter plot for b values
plt.figure(figsize=(12, 12))
plt.subplot(2, 1, 1)
for i in range(5):
    # plot each spike's b values separately to maintain distinct colors
    plt.scatter([num_prefix for j, num_prefix in enumerate(x) if j % 5 == i],
                [b for j, b in enumerate(y) if j % 5 == i], color=colors[i], label=f'Spike {i+1}')

plt.title('Value of B for Spikes 1-5 Across Numeric File Prefixes')
plt.xlabel('Numeric File Prefix')
plt.ylabel('B value')
plt.legend()
# plt.plot()
plt.show()
# # Plot the absorption_voltage data
# plt.figure(figsize=(12, 6))
# plt.plot(df['absorption_voltage'], label='Absorption Voltage', color='blue')
# plt.plot(df['field_voltage'], label='Field Voltage', color='blue')


# # Highlight the spikes on the plot
# plt.scatter(spike_indices, df.loc[spike_indices, 'absorption_voltage'], color='red', label='Spikes', zorder=5)

# # plt.scatter(spike_indices, df.loc[spike_indices, 'field_voltage'], color='red', label='Spikes', zorder=5)

# # Adding title and labels
# plt.title('Absorption Voltage and Detected Spikes')
# plt.xlabel('Index')
# plt.ylabel('Absorption Voltage')
# plt.legend()

# # Show the plot
# plt.show()