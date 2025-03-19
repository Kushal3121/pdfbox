from collections import defaultdict
from itertools import combinations

# Read the commits.txt file
with open('commits.txt', 'r') as file:
    lines = file.readlines()

# Parse the commits and files
commits = []
current_commit = None

for line in lines:
    line = line.strip()
    if line:  # Skip empty lines
        if len(line) == 40:  # Commit hash (assuming SHA-1)
            current_commit = line
            commits.append({"hash": current_commit, "files": []})
        else:  # File changed in the commit
            if line.endswith('.java'):  # Only consider Java files
                commits[-1]["files"].append(line)

# Dictionary to count co-changed files
co_changed_counts = defaultdict(int)

# Iterate through each commit
for commit in commits:
    files = commit['files']
    if len(files) >= 2:  # Only consider commits with at least 2 files
        # Generate all combinations of 2, 3, 4, or 5 files
        for r in range(2, 6):  # r = 2, 3, 4, 5
            for combo in combinations(files, r):
                co_changed_counts[combo] += 1

# Filter out combinations that occur less than 3 times
co_changed_files = {combo: count for combo, count in co_changed_counts.items() if count >= 3}

# Print the results
for combo, count in co_changed_files.items():
    print(f"Files: {combo}, Occurrences: {count}")