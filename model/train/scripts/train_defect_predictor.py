import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import cross_val_score, cross_val_predict, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score

# Load training data
df = pd.read_csv('training_data.csv')

# Clean missing values (especially in DIT)
df_clean = df.dropna(subset=['DIT'])

# Define features and target
X = df_clean[['WMC', 'LCOM', 'CBO', 'DIT']]
y = df_clean['Buggy']

# Initialize decision tree classifier (J48-like with entropy)
clf = DecisionTreeClassifier(criterion='entropy', random_state=42)

# 10-fold cross-validation setup
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
y_pred = cross_val_predict(clf, X, y, cv=cv)

# Fit the classifier on full data for tree visualization
clf.fit(X, y)

# Evaluation
accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred)
recall = recall_score(y, y_pred)
conf_matrix = confusion_matrix(y, y_pred)
report = classification_report(y, y_pred)
tree_rules = export_text(clf, feature_names=list(X.columns))

# Save output to results.txt
with open("training_results.txt", "w") as f:
    f.write("=== Defect Prediction Results ===\n")
    f.write(f"Accuracy : {accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall   : {recall:.4f}\n\n")
    
    f.write("=== Confusion Matrix ===\n")
    f.write(f"{conf_matrix}\n\n")
    
    f.write("=== Classification Report ===\n")
    f.write(f"{report}\n\n")
    
    f.write("=== Decision Tree Rules ===\n")
    f.write(tree_rules)
