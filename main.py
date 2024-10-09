import traceback
import time
import argparse
import lib.labels as labels

from threading import Event, Lock
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from lib.controller import Controller
from fischertechnik.controller.Motor import Motor

txt = None  # type: Controller

queue = Queue()
mutex_input = Lock()

executor = ThreadPoolExecutor()

SLEEP_TIME = 0.001


def prelude():
    """Prelude of the program."""
    print("prelude")

    global txt # , model
    txt = Controller()
    # model = ObjectDetector("train/model.tflite", "train/labels.txt")


def setup():
    """Setup the robot before the main loop."""
    print("setup")

    # turn on LEDs for the phototransistors
    txt.ext.bio_led.set_brightness(512)
    txt.ext.np_led.set_brightness(512)
    txt.ext.rec_led.set_brightness(512)
    txt.ext.front_led.set_brightness(512)


def loop(i):
    """Main loop of the program."""
    print("loop %d" % i)
    # for each index, start a new thread to wait for the waste to pass by the phototransistor
    segregate_waste(i)


def move_waste():
    """Move the waste to the sorting area."""
    txt.ext.front_motor.set_speed(256, Motor.CCW)
    txt.ext.back_motor.set_speed(256, Motor.CCW)
    txt.ext.front_motor.start_sync(txt.ext.back_motor)


def segregate_waste(i):
    """Segregates waste into its proper containers."""
    wait_for_pt_pass(txt.main.front_pt)

    target_map = {
        (True, True): (labels.BIO, wait_for_bio),
        (True, False): (labels.NP, wait_for_np),
        (False, True): (labels.REC, wait_for_rec),
        (False, False): (labels.PLASTIC, wait_for_plastic),
    }

    label, target = target_map[(i % 2 == 0, i % 3 == 0)]

    queue.put((label, i))
    executor.submit(target, i)


def wait_for_queue(label, n, pt):
    """Waits for the specific item in the queue and triggers the piston."""
    while True:
        try:
            if queue.queue[0] == (label, n):
                wait_for_pt_pass(pt)
                queue.get()
                break
        except IndexError:
            pass
        Event().wait(SLEEP_TIME)


def wait_for_pt_pass(pt):
    while pt.is_dark():
        Event().wait(SLEEP_TIME)
    while pt.is_bright():
        Event().wait(SLEEP_TIME)


def wait_for_bio(n):
    """Wait for the bio waste to pass by the phototransistor."""
    wait_for_queue(labels.BIO, n, txt.main.bio_pt)
    use_piston(txt.main.bio_valve)


def wait_for_np(n):
    """Wait for the non-plastic waste to pass by the phototransistor."""
    wait_for_queue(labels.NP, n, txt.main.np_pt)
    use_piston(txt.main.np_valve)


def wait_for_rec(n):
    """Wait for the recyclable waste to pass by the phototransistor."""
    wait_for_queue(labels.REC, n, txt.main.rec_pt)
    use_piston(txt.main.rec_valve)


def wait_for_plastic(n):
    """Wait for the plastic waste to pass by the recyclable phototransistor."""
    wait_for_queue(labels.PLASTIC, n, txt.main.rec_pt)
    Event().wait(1.5)


def use_piston(valve):
    """Use the piston to sort the waste."""
    with mutex_input:
        txt.ext.back_motor.stop_sync(txt.ext.front_motor)

        txt.main.compressor.on()
        valve.on()
        time.sleep(0.25)
        txt.main.compressor.off()
        valve.off()


def test_outputs():
    print("Testing outputs...")
    input_loop()


def handle_motor(motor, speed=512):
    """Handles motor start/stop based on its current state."""
    if not motor.is_running():
        motor.set_speed(speed)
        motor.start()
    else:
        motor.stop()

def handle_valve(valve):
    """Handles valve on/off based on its current state."""
    if valve.is_off():
        valve.on()
    else:
        valve.off()


def handle_led(led):
    """Handles LED on/off based on its current state."""
    if led.is_off():
        led.set_brightness(512)
    else:
        led.set_brightness(0)


def input_loop():
    compressor = False
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
        w = input("> ").strip()
        if w in command_map:
            command_map[w]()
        elif w == "c":
            compressor = not compressor
            if compressor:
                txt.main.compressor.on()
            else:
                txt.main.compressor.off()
        elif w == "q":
            break
        else:
            print("Unrecognized %s" % w)


def main():
    prelude()

    # parse arguments (-i/--debug-input, -m/--debug-model)
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--debug-input", action="store_true")
    args = parser.parse_args()

    if args.debug_input:
        test_outputs()
    else:
        setup()
        # wait until weight sensor is pressed
        while not txt.main.push_button.is_closed():
            pass

        move_waste()
        while True:
            loop()


try:
    main()
except Exception:
    print(traceback.format_exc())
