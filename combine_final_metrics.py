import pandas as pd
import os

# Path to your folder containing the CSV files
folder_path = 'final_metrics'

# List all the CSV files in the folder (assuming the files start with 'metrics_' and end with '.csv')
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv') and f.startswith('metrics_')]

# Sort the files by version number in the filename
csv_files.sort(key=lambda x: [int(i) for i in x.split('_')[1].split('.')[1:]])  # Extract and sort based on version

# Initialize an empty list to hold the DataFrames
dfs = []

# Iterate over each CSV file
for file in csv_files:
    # Read the CSV file into a DataFrame
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    
    # Append the DataFrame to the list
    dfs.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('training_data.csv', index=False)

print('CSV files successfully merged into combined_training_data.csv')
