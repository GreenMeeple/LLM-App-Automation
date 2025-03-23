import argparse
import sys
import os
import uiautomator2 as u2
from ordered_set import OrderedSet
from lxml import etree

from util.automation import *
from util.log import log

from data.devices import *
from data.prompts.jailbreak import short_DAN, long_DAN, STAN, tasks, tasks_debug
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Example: python main.py --app ai.character.app --name c.ai --emulator --rand --test
parser = argparse.ArgumentParser(description="Automate chatbot interaction with an emulator or device.")
parser.add_argument("--app", type=str, default="com.codespaceapps.aichat", help="Specify the chatbot application package name.")
parser.add_argument("--name", type=str, default="chatbot.assistant", help="Specify the app name for xml output.")
parser.add_argument('--emulator', type=int, default=0, help="0 = physical, rest are emulator")
args = parser.parse_args()

## Enter your own device id found on 'adb devices'
if __name__ == "__main__":
    device = emulators[args.emulator]
    create_session(args.app, args.name, device)
    for message_box in d(className="android.widget.EditText"):
        message_box.set_text(long_DAN)
    s = message_box.sibling(resourceIdMatches=".*[s|S]en[t|d].*")
    if s:
        s[-1].click()