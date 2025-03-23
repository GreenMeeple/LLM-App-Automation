# LLM-App-Automation

## Overview

**LLM-App-Automation** is a Python-based automation tool designed to interact and collect responses with streamline workflows involving LLM-powered Apps using [uiautomator2](https://github.com/openatx/uiautomator2). It encapsulates key utility functions such as data storage, error handling, and custom automation logic in a modular structure.

## Features

- 🔧 Modular utility scripts for:
  - Storage management (`storage.py`)
  - Custom automation (`automation.py`, `rainbow.py`)
  - Error handling (`tasks_reset.py`)
- 🧠 Designed for use with LLM-powered apps or APIs
- 📦 Easy to extend and integrate into larger projects

---

**[Getting Started](#getting-started)**

- **[Prerequisites](#prerequisites)**
- **[Installation](#installation)**

**[Usage](#usage)**

- **[Arguments](#arguments)**
- **[Other Settings](#other-settings)**

**[Project Details](#project-details)**

- **[Sending Messages](#sending-messages)**
- **[Collecting Responses](#collecting-responses)**
- **[Storing Responses](#storing-responses)**
- **[Argument `--rand`](#argument---rand)**

**[Project Structure](#project-structure)**

**[Roadmap](#roadmap)**

**[References](#references)**

## Getting Started

### Prerequisites

- Python 3.9+ , `pip` for installing packages

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/LLM-App-Automation.git
    cd LLM-App-Automation
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Customize the emulator file `data/devices.py`

    Create a file `data/devices.py` to contain your device name. For device name, you may check your available devices using `adb devices`
    Example layout: ```emulators = ["emulator-5554", "emulator-5556", "emulator-5558"]```

## Usage

> Your first Run: `python main.py`

### Arguments

```python
python main.py --app [AppId] --name [csv_name] --emulator --rand
```

- `--app [AppId]` (Default: "ai.character.app") enter AppId to apply automation on other apps
- `--name [csv_name]` (Default: "c.ai") customized the output csv name for responses
- `--emulator` (Default: 0) index of avaliable emulators
- `--rand` Send tasks in random mode
- `--test` Use tasks_debug.json for test run

In `util/automation.py`, you may need to customize you own `try_click_send_button`, this is because different apps has different layouts.
You may modify the `create_session` function generate `check.xml` file to inspect.

### Other settings

- **Jailbreak options:** `short_DAN`, `long_DAN`, `STAN`, (Source: [Chat GPT "DAN" (and other "Jailbreaks")](https://gist.github.com/coolaj86/6f4f7b30129b0251f61fa7baaa881516))

## Project Details

### Sending Messages

1. Retrieve jailbreak prompt and tasks list from `data/prompts/jailbreak.py`

2. Locate the message box (EditText)

    ```python
    message_box = d(className="android.widget.EditText", instance=0)
    ```

3. Send the message

### Collecting Responses

1. Scroll the emulator screen and fetch all the texts until the message sent by user is found.

2. Store all collected responses into an ordered set

3. Remove duplicates from `collected_responses` or the message itself

    ```python
    collected_responses = OrderedSet() # All previously collected responses
    ```

4. Add the new collected responses into `collected_responses`

### Storing Responses

1. During the run, responses are stored in seperate `.txt` file

    ```python
    txt_folder_path = os.path.join("data/textfiles/", f'{args.name}_rand') if args.rand else os.path.join("data/textfiles/", f'{args.name}')
    ```

2. All unprocessed tasks will also be stored in case of error occured

    ```python
    unprocessed_file_path = os.path.join("data/temp/", f"{args.name}_unprocessed.json")
    ```

3. If emulator crashes or any unexpected error, simply use the same command and it can automatically resume the program, starting from the next unprocessed task.

4. When all tasks are sent (`unprocessed.json` should be empty), `unprocessed.json` will be deleted and all `.txt` files will be converted into a single `.csv` file.

### Argument `--rand`

- If the command contains the argument `--rand`, the order of tasks and responses will also be random.

  - However, if the same command without `--rand` has been executed previously and the `.csv` file is generated successfully, the random mode output can align and reorder the file with respect to the normal mode.

## Project Structure

```bash
LLM-App-Automation/
├── main.py # Entry point of the application 
├── requirements.txt # Python dependencies 
├── util/ 
│   ├── automation.py # Core automation logic   
│   ├── log.py # Logging utilities 
│   ├── storage.py # Local/remote storage handling 
│   └── rainbow.py # Rainbow table for app interfaces handling
├── debug/ 
│   ├── interface_tester.py # Test for new interfaces
│   ├── tasks_reset.py # Regenerate unprocessed.json when error occured
├── data/ 
│   ├── prompts # parsing jailbreak prompts and tasks list
│   │   ├── jailbreak.py # Store jailbreak prompts and tasks list
│   │   ├── tasks_debug.json # Small set of tasks for test run
│   │   └── tasks.json # Full set of tasks 
│   ├── devices.py # List of emulator
│   └── responses # Folder to store responses
└── .gitignore # Git ignore rules
```

## Roadmap

- [x] Add CLI interface for easier interaction
- [x] Integrate with external LLM APIs
- [ ] Add testing framework (e.g., pytest)
- [x] Improve logging and monitoring (util/log.py)

## References

[Chat GPT "DAN" (and other "Jailbreaks")](https://gist.github.com/coolaj86/6f4f7b30129b0251f61fa7baaa881516)

[uiautomator2](https://github.com/openatx/uiautomator2)