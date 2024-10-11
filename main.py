import argparse
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Event, Lock

from fischertechnik.controller.Motor import Motor
from lib.controller import Controller
import lib.labels as waste_labels

# Global Variables and Initialization
txt = None  # type: Controller
waste_queue = Queue()
output_mutex = Lock()
input_mutex = Lock()

executor = ThreadPoolExecutor()

# Events for waste detection
front_waste_event = Event()
bio_waste_event = Event()
np_waste_event = Event()
recyclable_waste_event = Event()
plastic_waste_event = Event()


def phototransistor_event_loop(waste_event, phototransistor):
    """Monitors the phototransistor and triggers the event when waste is detected."""
    while True:
        if phototransistor.is_dark():
            while not phototransistor.is_bright():
                pass
            waste_event.set()


def initialize_controller():
    """Initializes the robot controller."""
    global txt
    txt = Controller()
    print("Controller initialized.")


def configure_robot():
    """Configures the robot components before starting the main loop."""
    print("Configuring robot...")

    # Set brightness for LEDs and turn on the compressor
    txt.ext.bio_led.set_brightness(512)
    txt.ext.np_led.set_brightness(512)
    txt.ext.rec_led.set_brightness(512)
    txt.ext.front_led.set_brightness(512)

    txt.main.compressor.on()

    # Start phototransistor event loops
    executor.submit(phototransistor_event_loop, bio_waste_event, txt.main.bio_pt)
    executor.submit(phototransistor_event_loop, np_waste_event, txt.main.np_pt)
    executor.submit(phototransistor_event_loop, recyclable_waste_event, txt.main.rec_pt)
    executor.submit(phototransistor_event_loop, plastic_waste_event, txt.main.rec_pt)
    executor.submit(phototransistor_event_loop, front_waste_event, txt.ext.front_pt)


def safe_print(*args, **kwargs):
    """Thread-safe print function."""
    with output_mutex:
        print(*args, **kwargs)


def process_waste_item(item_index):
    """Main loop to process each waste item."""
    safe_print("Processing waste item {}".format(item_index))
    classify_and_sort_waste(item_index)


def move_waste_to_sorting_area():
    """Moves waste to the sorting area."""
    txt.ext.front_motor.set_speed(200, Motor.CCW)
    txt.ext.back_motor.set_speed(200, Motor.CCW)
    txt.ext.front_motor.start()
    txt.ext.back_motor.start()


def classify_and_sort_waste(item_index):
    """Classifies the waste type and directs it to the appropriate container."""
    waste_sorting_map = {
        (True, True): (waste_labels.BIO, handle_bio_waste),
        (True, False): (waste_labels.NP, handle_np_waste),
        (False, True): (waste_labels.REC, handle_recyclable_waste),
        (False, False): (waste_labels.PLASTIC, handle_plastic_waste),
    }

    waste_label, sorting_function = waste_sorting_map[(item_index % 2 == 0, item_index % 3 == 0)]

    wait_for_waste_event(front_waste_event) # Wait for waste to reach the front phototransistor
    waste_queue.put((waste_label, item_index))
    safe_print("{}: pushed {} to the queue".format(item_index, waste_label))
    executor.submit(sorting_function, item_index)


def wait_for_queue_item(waste_label, item_index, waste_event):
    """Waits for a specific waste item in the queue and triggers the sorting piston when detected."""
    safe_print("{}: waiting for {}".format(item_index, waste_label))

    while True:
        if waste_queue.queue and waste_queue.queue[0] == (waste_label, item_index):
            wait_for_waste_event(waste_event)
            safe_print("{}: {} passed".format(item_index, waste_label))
            waste_queue.get()
            waste_queue.task_done()
            break


def wait_for_waste_event(waste_event):
    """Waits for the waste detection event."""
    waste_event.wait()
    waste_event.clear()


def handle_bio_waste(item_index):
    """Handles bio-waste sorting."""
    wait_for_queue_item(waste_labels.BIO, item_index, bio_waste_event)
    activate_sorting_piston(txt.main.bio_valve)


def handle_np_waste(item_index):
    """Handles non-plastic waste sorting."""
    wait_for_queue_item(waste_labels.NP, item_index, np_waste_event)
    activate_sorting_piston(txt.main.np_valve)


def handle_recyclable_waste(item_index):
    """Handles recyclable waste sorting."""
    wait_for_queue_item(waste_labels.REC, item_index, recyclable_waste_event)
    activate_sorting_piston(txt.main.rec_valve)


def handle_plastic_waste(item_index):
    """Handles plastic waste sorting."""
    wait_for_queue_item(waste_labels.PLASTIC, item_index, plastic_waste_event)
    time.sleep(1)


def activate_sorting_piston(valve):
    """Activates the piston to sort the waste."""
    with input_mutex:
        txt.ext.back_motor.stop_sync(txt.ext.front_motor)

        valve.on()
        time.sleep(0.33)
        valve.off()

        move_waste_to_sorting_area()


def handle_motor(motor, speed=512):
    """Starts or stops the motor based on its current state."""
    if not motor.is_running():
        motor.set_speed(speed)
        motor.start()
    else:
        motor.stop()


def handle_valve(valve):
    """Opens or closes the valve based on its current state."""
    if valve.is_off():
        valve.on()
    else:
        valve.off()


def handle_led(led):
    """Toggles the LED on or off."""
    if led.is_off():
        led.set_brightness(512)
    else:
        led.set_brightness(0)


def input_loop():
    """Handles user input to control the system."""
    compressor_active = False
    command_map = {
        "fm": lambda: handle_motor(txt.ext.front_motor),
        "bm": lambda: handle_motor(txt.ext.back_motor),
        "bi": lambda: handle_valve(txt.main.bio_valve),
        "ni": lambda: handle_valve(txt.main.np_valve),
        "ri": lambda: handle_valve(txt.main.rec_valve),
        "fl": lambda: handle_led(txt.ext.front_led),
        "bl": lambda: handle_led(txt.ext.bio_led),
        "nl": lambda: handle_led(txt.ext.np_led),
    }

    while True:
        command = input("> ").strip()
        if command in command_map:
            command_map[command]()
        elif command == "c":
            compressor_active = not compressor_active
            if compressor_active:
                txt.main.compressor.on()
            else:
                txt.main.compressor.off()
        elif command == "q":
            break
        else:
            print("Unrecognized command: {}".format(command))


def main():
    """Main entry point of the program."""
    initialize_controller()

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--debug-input", action="store_true")
    args = parser.parse_args()

    if args.debug_input:
        input_loop()
    else:
        configure_robot()
        move_waste_to_sorting_area()

        item_index = 1
        while True:
            process_waste_item(item_index)
            item_index += 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
