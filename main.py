from threading import Thread, Lock
from queue import Queue
import traceback
import time
import argparse
from lib.controller import Controller
from lib.object_detector import ObjectDetector
from fischertechnik.controller.Motor import Motor
import lib.labels as labels

txt = None  # type: Controller
model = None  # type: ObjectDetector

queue = Queue()
mutex_input = Lock()

i = 0
threads = []


def prelude():
    """Prelude of the program."""
    print("prelude")

    global txt, model
    txt = Controller()
    model = ObjectDetector("train/model.tflite", "train/labels.txt")


def setup():
    """Setup the robot before the main loop."""
    print("setup")

    # turn on LEDs for the phototransistors
    txt.ext.bio_led.set_brightness(512)
    txt.ext.np_led.set_brightness(512)
    txt.ext.rec_led.set_brightness(512)
    txt.ext.front_led.set_brightness(512)


def loop():
    """Main loop of the program."""
    print("loop")
    # for each index, start a new thread to wait for the waste to pass by the phototransistor
    segregate_waste()


def move_waste():
    """Move the waste to the sorting area."""
    txt.ext.front_motor.set_speed(256, Motor.CCW)
    txt.ext.back_motor.set_speed(256, Motor.CCW)
    txt.ext.front_motor.start_sync(txt.ext.back_motor)


def segregate_waste():
    """Segregates waste into its proper containers."""
    global i
    wait_for_pt_pass(txt.main.front_pt)
    i += 1
    target = None

    div2 = i % 2 == 0
    div3 = i % 3 == 0

    if div2 and div3:  # if divisible by both 2 and 3
        queue.put(labels.BIO)
        target = wait_for_bio
    elif div2:
        queue.put(labels.NP)
        target = wait_for_np
    elif div3:
        queue.put(labels.REC)
        target = wait_for_rec
    else:
        queue.put(labels.PLASTIC)
        target = wait_for_plastic

    t = Thread(target=target)
    t.start()
    threads.append(t)


def wait_for_pt_pass(pt):
    while pt.is_dark():
        pass
    while pt.is_bright():
        pass


def wait_for_bio():
    """Wait for the bio waste to pass by the phototransistor."""
    while queue[0] != labels.BIO:
        wait_for_pt_pass(txt.main.bio_pt)
    use_piston(txt.main.bio_valve, txt.main.np_valve)
    queue.get()


def wait_for_np():
    """Wait for the non-plastic waste to pass by the phototransistor."""
    while queue[0] != labels.NP:
        wait_for_pt_pass(txt.main.np_pt)
    use_piston(txt.main.np_valve)
    queue.get()


def wait_for_rec():
    """Wait for the recyclable waste to pass by the phototransistor."""
    while queue[0] != labels.REC:
        wait_for_pt_pass(txt.main.rec_pt)
    use_piston(txt.main.rec_valve)
    queue.get()


def wait_for_plastic():
    """Wait for the plastic waste to pass by the recyclable phototransistor."""
    while queue[0] != labels.PLASTIC:
        wait_for_pt_pass(txt.main.rec_pt)
    time.sleep(2)
    queue.get()


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


def test_model():
    # test the model on the camera feed
    print("Testing model...")
    while True:
        detected = model.process_image(txt.main.camera.get_frame())
        print(detected)
        time.sleep(0.5)


def input_loop():
    compressor = False
    while True:
        w = input("> ").strip()

        if w == "fm":
            if not txt.ext.front_motor.is_running():
                txt.ext.front_motor.set_speed(512)
                txt.ext.front_motor.start()
            else:
                txt.ext.front_motor.stop()
        elif w == "bm":
            if not txt.ext.back_motor.is_running():
                txt.ext.back_motor.set_speed(512)
                txt.ext.back_motor.start()
            else:
                txt.ext.back_motor.stop()
        elif w == "bi":
            if txt.main.bio_valve.is_off():
                txt.main.bio_valve.on()
            else:
                txt.main.bio_valve.off()
        elif w == "ni":
            if txt.main.np_valve.is_off():
                txt.main.np_valve.on()
            else:
                txt.main.np_valve.off()
        elif w == "ri":
            if txt.main.rec_valve.is_off():
                txt.main.rec_valve.on()
            else:
                txt.main.rec_valve.off()
        elif w == "c":
            if not compressor:
                compressor = True
                txt.main.compressor.on()
            else:
                compressor = False
                txt.main.compressor.off()
        elif w == "fl":
            if txt.ext.front_led.is_off():
                txt.ext.front_led.set_brightness(512)
            else:
                txt.ext.front_led.set_brightness(0)
        elif w == "bl":
            if txt.ext.bio_led.is_off():
                txt.ext.bio_led.set_brightness(512)
            else:
                txt.ext.bio_led.set_brightness(0)
        elif w == "nl":
            if txt.ext.np_led.is_off():
                txt.ext.np_led.set_brightness(512)
            else:
                txt.ext.np_led.set_brightness(0)
        elif w == "rl":
            if txt.ext.rec_led.is_off():
                txt.ext.rec_led.set_brightness(512)
            else:
                txt.ext.rec_led.set_brightness(0)
        else:
            print("Unrecognized %s" % w)


try:
    prelude()

    # parse arguments (-i/--debug-input, -m/--debug-model)
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--debug-input", action="store_true")
    parser.add_argument("-m", "--debug-model", action="store_true")
    args = parser.parse_args()

    if args.debug_input:
        test_outputs()
    elif args.debug_model:
        test_model()
    else:
        setup()
        # wait until weight sensor is pressed
        while not txt.main.push_button.is_closed():
            pass

        move_waste()
        while True:
            loop()
except Exception:
    print(traceback.format_exc())
