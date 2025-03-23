import os
import pandas as pd
import csv
import json

# Save updated unprocessed tasks
def save_unprocessed_tasks(unprocessed_file_path, prompts):
    with open(unprocessed_file_path, "w") as file:
        json.dump(prompts, file, indent=4)

def response_to_txt(prompt, response, directory, file_name):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)
    with open(file_path, mode='w+', encoding='utf-8') as f:
        formatted_response = '\n'.join(response)
        f.write(prompt)
        f.write('\n-----------------------\n')
        f.write(formatted_response)

def txt_to_csv(txt_folder_path, csv_file_path):
    # Initialize an empty list to store data
    data = []

    # Loop through TXT files in sorted numeric order
    for filename in sorted(os.listdir(txt_folder_path), key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else float('inf')):
        if filename.endswith(".txt"):  # Process only TXT files
            txt_file_path = os.path.join(txt_folder_path, filename)

            # Read the TXT file
            with open(txt_file_path, "r", encoding="utf-8") as file:
                txt_content = file.readlines()

            # Extract prompt and response
            if len(txt_content) > 2:
                prompt = txt_content[0].strip()  # First line is the prompt
                response = "".join(txt_content[2:]).strip()  # Skip separator, take the rest as response

                # Append extracted data
                data.append({"Prompt": prompt, "Response": response})

    # Create a DataFrame and append to CSV
    if data:
        df = pd.DataFrame(data)
        df.to_csv(csv_file_path, index=False, mode='w', encoding='utf-8')  # 'w' to overwrite, use 'a' for append

    print(f"CSV file saved as {csv_file_path}")

def rand_csv_align(csv_file_path, csv_rand_file_path):

    # Load the CSV files
    df_original = pd.read_csv(csv_file_path)   # Original CSV
    df_random = pd.read_csv(csv_rand_file_path)  # Randomized CSV

    # Ensure the column names match (adjust if necessary)
    key_column = "Prompt"  # Column to align on (modify if needed)

    # Merge the shuffled DataFrame into the original order
    df_aligned = df_original[[key_column]].merge(df_random, on=key_column, how="left")

    # Save the aligned CSV
    df_aligned.to_csv(csv_rand_file_path, index=False)

    print("CSV files have been aligned successfully!")
