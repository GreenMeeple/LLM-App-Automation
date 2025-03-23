import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
txt_directory = "data/textfiles/temp"  # Set the correct path to your TXT files
json_file = "data/temp/data.json" # JSON file to store the first lines

# Get sorted list of TXT files (numerically sorted)
txt_files = sorted(
    [f for f in os.listdir(txt_directory) if f.endswith(".txt")],
    key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else float("inf")
)

# List to store first lines
first_lines = []

# Loop through TXT files
for filename in txt_files:
    txt_file_path = os.path.join(txt_directory, filename)

    # Read the first line of the TXT file
    with open(txt_file_path, "r", encoding="utf-8") as file:
        first_line = file.readline().strip()
        first_lines.append(first_line)

# Write list to JSON
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(first_lines, f, indent=4)

print(f"✅ JSON saved to {json_file}")
