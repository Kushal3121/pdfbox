import os
import pandas as pd
import re
from subprocess import check_output

# === CONFIGURATION ===
versions = ["2.0.26", "2.0.27", "2.0.28", "2.0.29", "2.0.30"]
input_folder = "updated_metrics/"
output_folder = "final_metrics/"
repo_path = "/Users/kushalc/Desktop/UTD/Study/Semester 2/CS6356 - SE/HW/HW4/pdfbox"

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# === FUNCTION TO DETERMINE IF A COMMIT MESSAGE INDICATES A BUG ===
def is_buggy(commit_msg):
    bug_keywords = ["fix", "bug", "issue", "error", "fail"]
    if any(keyword in commit_msg.lower() for keyword in bug_keywords):
        if re.search(r"PDFBOX-\d+", commit_msg):
            return True
    return False

# === FUNCTION TO CONVERT CLASS NAME TO FILE PATH ===
def get_file_path(class_name):
    """
    Convert a fully qualified class name to its corresponding file path in the repository.
    """
    class_name_cleaned = class_name.split("-")[0]  # Remove version number if present

    # Determine module path
    if class_name_cleaned.startswith("org.apache.fontbox"):
        module_path = "fontbox/src/main/java/"
    elif class_name_cleaned.startswith("org.apache.pdfbox"):
        module_path = "pdfbox/src/main/java/"
    elif class_name_cleaned.startswith("org.apache.xmpbox"):
        module_path = "xmpbox/src/main/java/"
    elif class_name_cleaned.startswith("org.apache.preflight"):
        module_path = "preflight/src/main/java/"
    elif class_name_cleaned.startswith("org.apache.tools"):
        module_path = "tools/src/main/java/"
    else:
        return None  

    # Convert class name to file path
    relative_path = class_name_cleaned.replace(".", "/") + ".java"

    # **Exclude test files**
    if "/test/" in module_path or "/test/" in relative_path or "Test" in relative_path:
        return None  

    return module_path + relative_path  

# === FUNCTION TO GET COMMITS FOR A CLASS FILE ===
def get_commits_for_class(version, class_file):
    if not class_file:
        return ""

    command = f"git log --pretty=format:'%H %s' version-{version} -- {class_file}"
    try:
        commit_logs = check_output(command, shell=True, cwd=repo_path).decode("utf-8")
    except Exception as e:
        print(f"Error retrieving commits for {class_file}: {e}")
        return ""
    return commit_logs

# === FUNCTION TO EXTRACT BUGGY INFORMATION FROM COMMITS ===
def extract_buggy_info(version, class_file):
    commits = get_commits_for_class(version, class_file)
    buggy = 0  

    if commits:
        for commit in commits.split("\n"):
            commit_parts = commit.split(" ", 1)
            if len(commit_parts) > 1:
                commit_msg = commit_parts[1]  
                if is_buggy(commit_msg):
                    buggy = 1
                    break  

    return buggy

# === FUNCTION TO PROCESS EACH VERSION ===
def process_version(version):
    input_file = f"{input_folder}metrics_{version}.csv"
    output_file = f"{output_folder}metrics_{version}_with_buggy.csv"

    df = pd.read_csv(input_file)

    # === IDENTIFY CLASS COLUMN ===
    class_col = [col for col in df.columns if 'class' in col.lower()][0]

    # **Keep class column as is**
    df["Buggy"] = df[class_col].apply(lambda class_name: extract_buggy_info(version, get_file_path(class_name)))

    # === SAVE UPDATED CSV ===
    df.to_csv(output_file, index=False)
    print(f"✅ Updated CSV with 'buggy' column for version {version} saved as: {output_file}")

# === PROCESS ALL VERSIONS ===
for version in versions:
    process_version(version)
