from collections import defaultdict, Counter
import itertools
import glob
import csv

# Initialize data structures
file_cochanges = defaultdict(set)  # Maps files to sets of commits they appear in
commit_files = defaultdict(set)    # Maps commits to sets of files changed in that commit

# Get all split files (changeLog_part_*.txt)
split_files = glob.glob("changeLog_part_*.txt")

# Process each split file
for split_file in split_files:
    print(f"Processing {split_file}...")
    with open(split_file, "r") as file:
        lines = file.readlines()

    # Parse the file
    commit_hash = None
    files_changed = []

    for line in lines:
        line = line.strip()
        if line.startswith("Commit Hash:"):
            # Save the previous commit's data (if any)
            if commit_hash and files_changed:
                # Update file_cochanges and commit_files
                for file_path in files_changed:
                    file_cochanges[file_path].add(commit_hash)
                commit_files[commit_hash] = set(files_changed)

            # Reset for the next commit
            commit_hash = line.split(": ")[1]
            files_changed = []
        elif line.startswith("Files Changed:"):
            # Skip the "Files Changed:" line
            continue
        elif line:  # File changes (A, M, D)
            file_path = line.split("\t")[1]  # Extract the file path
            if file_path.endswith(".java"):  # Only consider Java files
                files_changed.append(file_path)

# Find co-changed files
def find_cochanged_files(file_cochanges, commit_files, set_size, min_occurrences):
    cochanged_sets = Counter()  # Count occurrences of each co-changed set
    cochanged_commits = defaultdict(list)  # Maps co-changed sets to their commits

    # Iterate through all commits
    for commit, files in commit_files.items():
        if len(files) >= set_size:
            # Generate all combinations of files of the given set size
            for file_set in itertools.combinations(files, set_size):
                cochanged_sets[file_set] += 1
                cochanged_commits[file_set].append(commit)

    # Filter sets that occur at least min_occurrences times
    result = []
    for file_set, count in cochanged_sets.items():
        if count >= min_occurrences:
            result.append({
                "files": file_set,
                "commits": cochanged_commits[file_set]
            })
    return result

# Find co-changed sets of 2, 3, 4, and 5 files
cochanged_2 = find_cochanged_files(file_cochanges, commit_files, 2, 3)
cochanged_3 = find_cochanged_files(file_cochanges, commit_files, 3, 3)
cochanged_4 = find_cochanged_files(file_cochanges, commit_files, 4, 3)
cochanged_5 = find_cochanged_files(file_cochanges, commit_files, 5, 3)

# Save results to a CSV file
output_csv = "cochanged_files.csv"
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(["List of co-changed files", "List of commits"])
    # Write co-changed sets of 2 files
    for entry in cochanged_2:
        files = "\n".join([f"{i+1}. {file}" for i, file in enumerate(entry["files"])])
        commits = "\n".join([f"{i+1}. {commit}" for i, commit in enumerate(entry["commits"])])
        writer.writerow([files, commits])
    # Write co-changed sets of 3 files
    for entry in cochanged_3:
        files = "\n".join([f"{i+1}. {file}" for i, file in enumerate(entry["files"])])
        commits = "\n".join([f"{i+1}. {commit}" for i, commit in enumerate(entry["commits"])])
        writer.writerow([files, commits])
    # Write co-changed sets of 4 files
    for entry in cochanged_4:
        files = "\n".join([f"{i+1}. {file}" for i, file in enumerate(entry["files"])])
        commits = "\n".join([f"{i+1}. {commit}" for i, commit in enumerate(entry["commits"])])
        writer.writerow([files, commits])
    # Write co-changed sets of 5 files
    for entry in cochanged_5:
        files = "\n".join([f"{i+1}. {file}" for i, file in enumerate(entry["files"])])
        commits = "\n".join([f"{i+1}. {commit}" for i, commit in enumerate(entry["commits"])])
        writer.writerow([files, commits])

print(f"Results saved to {output_csv}")