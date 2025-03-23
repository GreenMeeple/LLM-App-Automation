import uiautomator2 as u2
from ordered_set import OrderedSet
from lxml import etree
from time import sleep
from util.log import log
from util.rainbow import *

d = None
collected_responses = OrderedSet()

def parse_tree(raw):
    return etree.fromstring(raw.encode("utf-8"))

def xml_generate(d, name):
    raw_xml = d.dump_hierarchy()
    with open(f"data/check_{name}.xml", 'w+', encoding='utf-8') as f:
        f.write(raw_xml)

    log.info(f"Session created for app {name}.")
    return d


def create_session(appId, name, emulator=None):
    global d
    if emulator:
        d = u2.connect(emulator)
    else:
        d = u2.connect()
    if not d:
        log.error("Failed to connect to the device.")
        return None
    _ = d.session(appId, attach=True)

    xml_generate(d, name)

def send_message(text, appId):
    log.info('Sending message...')
    # Input prompt
    message_box = d(className="android.widget.EditText", instance=0)
    if message_box:
        message_box.click()
        sleep(1.2)
        message_box.set_text(text)
    # For AskAI
    else: 
        d(description="Write your message").click()
        sleep(1)
        message_box = d(className="android.widget.EditText")
        message_box.set_text(text)

    sleep(1.2)
    log.info('Found msg box.')
    try_click_send_button(message_box, appId)
    log.info('Clicked send button.')

    # Works for Physical device but sometimes create unexpected issue when finding textbox, use it carefully.
    d.press("back")

def collect_response(prompt, max_scrolls=5):
    sleep(20)
    log.info(f"Collecting results...")
    # for _ in range(max_scrolls):
    #     d.swipe_ext("up", scale=1.0)

    response = OrderedSet()
    for _ in range(max_scrolls):
        tree = parse_tree(d.dump_hierarchy())
        get_all_texts(tree, response)
        if prompt in response:
            log.info(f"Found the original prompt, stopping.")
            break
        d.swipe_ext("down", scale=1.0)
        sleep(1)

    # Trim out the user prompt + any known old lines
    response = trim_collected(response, prompt, collected_responses)

    collected_responses.update(response)
    log.info(f"Collected {len(response)}.")
    return response

def get_all_texts(root, texts):
    for element in root.iter():
        # Check and add inner text
        text_content = element.text.strip() if element.text else ""
        if text_content:
            texts.add(text_content)

        # Check and add text from "text" attribute
        text_attr = element.get('text', '').strip()
        if text_attr:
            texts.add(text_attr)

        # Check and add text from "text" attribute
        desc_attr = element.get('content-desc', '').strip()
        if desc_attr:
            texts.add(desc_attr)

def trim_collected(response, prompt, collected_responses=[]):
    for text in collected_responses:
        if text in response:
            response.remove(text)
    if prompt in response:
        response.remove(prompt)
    new_response = list(response)
    return new_response