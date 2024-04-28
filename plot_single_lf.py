import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import false

# Load the CSV file
df = pd.read_csv('4_18_24-OP/40kHz_R1000_PT10_D15.csv', header=None)

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
            spikes.append(
                (j-1, df.loc[j - 1, 'absorption_voltage'], df.loc[j - 1, 'field_voltage']))
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
    voltage_difs = [spike[2] -
                    central_absorption_voltage for spike in relevant_spikes]
    b_difs = [voltage*8.991*10**-3*11/0.1639 for voltage in voltage_difs]
    print(b_difs)

    # print("Adjusted Spike Data:", voltage_difs)


# # Plot the absorption_voltage data
plt.figure(figsize=(12, 6))
plt.plot(df['absorption_voltage'], label='Absorption Voltage', color='blue')
plt.plot(df['field_voltage'], label='Field Voltage', color='blue')


# Highlight the spikes on the plot
plt.scatter(spike_indices, df.loc[spike_indices,
            'absorption_voltage'], color='red', label='Spikes', zorder=5)

# plt.scatter(spike_indices, df.loc[spike_indices, 'field_voltage'], color='red', label='Spikes', zorder=5)

# Adding title and labels
plt.title('Absorption Voltage and Detected Spikes')
plt.xlabel('Index')
plt.ylabel('Absorption Voltage')
plt.legend()

# Show the plot
plt.show()
