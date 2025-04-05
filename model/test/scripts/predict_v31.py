import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# === Step 1: Load and prepare training data ===
df_train = pd.read_csv('training_data.csv')
df_train = df_train.dropna(subset=['DIT'])

X_train = df_train[['WMC', 'LCOM', 'CBO', 'DIT']]
y_train = df_train['Buggy']

# === Step 2: Train the model (same settings as before) ===
clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
clf.fit(X_train, y_train)

# === Step 3: Load top 75 classes from version 2.0.31 ===
df_31 = pd.read_csv('v31_top75.csv')
X_31 = df_31[['WMC', 'LCOM', 'CBO', 'DIT']]  # LOC is not used here

# === Step 4: Predict buggy status ===
df_31['Predicted_Buggy'] = clf.predict(X_31)

# === Step 5: Save prediction results ===
df_31.to_csv('v31_predictions.csv', index=False)
print("✅ Predictions saved to v31_predictions.csv")
