import argparse
import time
import traceback
import queue
import threading

from fischertechnik.controller.Motor import Motor
from lib.controller import Controller
import lib.labels as waste_labels

# Global Variables and Initialization
txt = None  # type: Controller
waste_queue = queue.Queue()
output_mutex = threading.Lock()
input_mutex = threading.Lock()


def wait_for_phototransistor(phototransistor):
    """Waits for the phototransistor to detect waste."""
    while not phototransistor.is_dark():
        time.sleep(0.01)
    while phototransistor.is_dark():
        time.sleep(0.01)


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
    txt.ext.front_motor.set_speed(375, Motor.CCW)
    txt.ext.back_motor.set_speed(200, Motor.CCW)
    txt.ext.front_motor.start()
    txt.ext.back_motor.start()


def classify_and_sort_waste(item_index):
    """Classifies the waste type and directs it to the appropriate container."""
    waste_sorting_map = {
        (True, False): (waste_labels.BIO, handle_bio_waste),
        (False, True): (waste_labels.NP, handle_np_waste),
        (True, True): (waste_labels.REC, handle_recyclable_waste),
        (False, False): (waste_labels.PLASTIC, handle_plastic_waste),
    }

    waste_label, sorting_function = waste_sorting_map[
        (item_index % 2 == 0, item_index % 3 == 0)
    ]

    wait_for_phototransistor(txt.main.front_pt)
    waste_queue.put((waste_label, item_index))
    safe_print("{}: pushed {} to the queue".format(item_index, waste_label))
    threading.Thread(target=sorting_function, args=(item_index,)).start()


def wait_for_queue_item(waste_label, item_index, phototransistor):
    """Waits for a specific waste item in the queue and triggers the sorting piston when detected."""
    safe_print("{}: waiting for {}".format(item_index, waste_label))

    while True:
        if waste_queue.queue and waste_queue.queue[0] == (waste_label, item_index):
            safe_print("{}: {} detected".format(item_index, waste_label))
            wait_for_phototransistor(phototransistor)
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
    wait_for_queue_item(waste_labels.BIO, item_index, txt.main.bio_pt)
    activate_sorting_piston(txt.main.bio_valve)


def handle_np_waste(item_index):
    """Handles non-plastic waste sorting."""
    wait_for_queue_item(waste_labels.NP, item_index, txt.main.np_pt)
    activate_sorting_piston(txt.main.np_valve)


def handle_recyclable_waste(item_index):
    """Handles recyclable waste sorting."""
    wait_for_queue_item(waste_labels.REC, item_index, txt.main.rec_pt)
    activate_sorting_piston(txt.main.rec_valve)


def handle_plastic_waste(item_index):
    """Handles plastic waste sorting."""
    wait_for_queue_item(waste_labels.PLASTIC, item_index, txt.main.rec_pt)
    time.sleep(1)


def activate_sorting_piston(valve):
    """Activates the piston to sort the waste."""
    with input_mutex:
        time.sleep(0.82)

        txt.ext.back_motor.stop()
        txt.ext.front_motor.stop()

        valve.on()
        time.sleep(0.75)
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

        item_index = 2
        while True:
            process_waste_item(item_index)
            item_index += 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
