import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Load training data
df = pd.read_csv('training_data.csv')
df = df.dropna(subset=['DIT'])

X = df[['WMC', 'LCOM', 'CBO', 'DIT']]
y = df['Buggy']

clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
clf.fit(X, y)

# Show feature importances
feature_importance = pd.Series(clf.feature_importances_, index=X.columns)
print("=== Feature Importance ===")
print(feature_importance.sort_values(ascending=False))
