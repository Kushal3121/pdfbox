import pandas as pd

# Load the CSV file you already have
df = pd.read_csv('metrics_v2.0.31.csv') 

# Sort by LOC descending and keep top 75
top75 = df.sort_values(by='LOC', ascending=False).head(75)

# Save to a new CSV file for prediction
top75.to_csv('v31_top75.csv', index=False)

print("Saved top 75 classes by LOC to v31_top75.csv")
