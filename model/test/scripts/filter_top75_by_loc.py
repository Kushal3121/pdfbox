import pandas as pd

# Load the CSV file
df = pd.read_csv('metrics_v2.0.31.csv')

# Ensure LOC is treated as numeric
df['LOC'] = pd.to_numeric(df['LOC'], errors='coerce')

# Drop rows with invalid LOC just in case
df = df.dropna(subset=['LOC'])

# Sort and extract top 75 by LOC
top75 = df.sort_values(by='LOC', ascending=False).head(75)

# Save to new CSV
top75.to_csv('v31_top75.csv', index=False)

print("Saved top 75 classes by LOC to v31_top75.csv")
