from time import sleep
import os
import argparse
import json
import random

from data.devices import *
from data.prompts.jailbreak import short_DAN, long_DAN, STAN, tasks, tasks_debug

from util.log import log
from util.automation import create_session, collect_response, send_message
from util.storage import response_to_txt, txt_to_csv, save_unprocessed_tasks, rand_csv_align

# Example: python main.py --app ai.character.app --name c.ai --emulator --rand --test
parser = argparse.ArgumentParser(description="Automate chatbot interaction with an emulator or device.")
parser.add_argument("--app", type=str, default="ai.character.app", help="Specify the chatbot application package name.")
parser.add_argument("--name", type=str, default="c.ai", help="Specify the app name for csv output.")
parser.add_argument('--emulator', type=int, default=0, help="0 = physical, rest are emulator")
parser.add_argument("--rand",  action='store_true', help="Run the prompt in random order with jailbreak prompt every 20 prompts")
parser.add_argument("--test",  action='store_true', help="Run the debug prompt for testing")
args = parser.parse_args()

## Enter your own device id found on 'adb devices'
if __name__ == "__main__":
    device = emulators[args.emulator]
    create_session(args.app, args.name, device)
    jailbreak = long_DAN # Possible jailbreak option: short_DAN, long_DAN, STAN

    txt_folder_path = os.path.join("data/textfiles/", f'{args.name}_rand') if args.rand else os.path.join("data/textfiles/", f'{args.name}')
    os.makedirs(txt_folder_path, exist_ok=True) # check if directory exists

    unprocessed_file_path = os.path.join("data/temp/", f"{args.name}_unprocessed.json")
    os.makedirs(os.path.dirname(unprocessed_file_path), exist_ok=True) # check if directory exists

    # If unprocessed_file_path exist, resume from previous run
    if os.path.exists(unprocessed_file_path):
        # Check existing .txt files and find the next available index
        existing_files = [f for f in os.listdir(txt_folder_path) if f.endswith(".txt")]
        existing_indices = [int(f.split(".")[0]) for f in existing_files if f.split(".")[0].isdigit()]
        next_index = max(existing_indices, default=0) + 1

        log.info("Resuming from unprocessed tasks...")
        with open(unprocessed_file_path, "r") as file:
            prompts = json.load(file)
    # Otherwise, start from the beginning
    else:
        log.info("Starting fresh task list...")
        prompts = tasks_debug[:] if args.test else tasks[:] # tasks = full list, tasks_debug = for debugging
        if args.rand:
            random.shuffle(prompts)

        # Start with jailbreaking prompt
        send_message(jailbreak, args.app)  
        sleep(10) # Wait for response, may vary from different apps
        response = collect_response(jailbreak)
        response_to_txt(jailbreak, response, txt_folder_path, "0.txt")
        next_index = 1
        
        # mostly needed for physical devices only
        # log.info("Buffer time in case any error.")
        # sleep(10)

    processed_tasks = []  # Track completed tasks separately

    # Start automation
    for idx, prompt in enumerate(prompts, start=next_index):
        send_message(prompt, args.app)
        response = collect_response(prompt)
        response_to_txt(prompt, response, txt_folder_path, f"{idx}.txt")

        # Sometimes emulator crashes unexpectedly, save progress for rerun
        processed_tasks.append(prompt)
        prompts = [task for task in prompts if task not in processed_tasks]
        save_unprocessed_tasks(unprocessed_file_path, prompts)

        # Run the prompt in random order with jailbreak prompt again every 20 prompts
        if(args.rand and idx%20==0):
            log.info("Refresh jailbreaking.")
            send_message(jailbreak, args.app)  # Possible jailbreak option: short_DAN, long_DAN, STAN
            response = collect_response(jailbreak)
            response_to_txt(jailbreak, response, txt_folder_path, "0.txt")

    # Convert to CSV after all tasks are done
    csv_file_path = os.path.join("data/responses/", f'{args.name}.csv')
    csv_rand_file_path = os.path.join("data/responses/", f'{args.name}_rand.csv')

    # define CSV path name
    if args.rand:
        txt_to_csv(txt_folder_path, csv_rand_file_path)
        # If a normal run is done, we can align the row of the random run as well
        if os.path.exists(csv_file_path):
            rand_csv_align(csv_file_path, csv_rand_file_path)
    else:
        txt_to_csv(txt_folder_path, csv_file_path)

    # Cleanup: Remove unprocessed file since all tasks are completed
    if os.path.exists(unprocessed_file_path):
        os.remove(unprocessed_file_path)
        log.info("All tasks completed. Removed unprocessed task list.")