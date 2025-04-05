import pandas as pd

# === CONFIGURATION ===
versions = ["2.0.26", "2.0.27", "2.0.28", "2.0.29", "2.0.30"]  # List of versions to process
input_folder = "raw_metrics/"  # Folder containing the input CSV files
output_folder = "metrics_updated/"  # Folder to save the updated CSV files

# === FUNCTION TO PROCESS EACH VERSION ===
def process_version(version):
    input_file = f"{input_folder}v{version}_metrics.csv"  # Input file path for the version
    output_file = f"{output_folder}metrics_{version}.csv"  # Output file path

    # === LOAD DATA ===
    df = pd.read_csv(input_file)

    # === ADD VERSION TO CLASS NAME ===
    class_col = [col for col in df.columns if 'class' in col.lower()][0]
    df["Class-Version"] = df[class_col].astype(str) + f"-{version}"

    # === REMOVE OLD 'Class' COLUMN AND RENAME 'Class-Version' ===
    df = df.drop(columns=[class_col])  # Drop the old class column
    df = df.rename(columns={"Class-Version": "Class"})  # Rename the new column

    # === REORDER COLUMNS: Class first ===
    cols = df.columns.tolist()
    cols = ["Class"] + [col for col in cols if col != "Class"]
    df = df[cols]

    # === SAVE UPDATED CSV ===
    df.to_csv(output_file, index=False)
    print(f"✅ Updated CSV for version {version} saved as: {output_file}")

# === LOOP THROUGH ALL VERSIONS ===
for version in versions:
    process_version(version)
