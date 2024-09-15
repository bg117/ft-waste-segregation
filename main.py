import threading
import traceback
import time
import sys
import argparse
from lib.controller import Controller
from lib.object_detector import ObjectDetector
from fischertechnik.controller.Motor import Motor
import lib.labels as labels

txt = None  # type: Controller
model = None  # type: ObjectDetector


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
    txt.ext.plastic_led.set_brightness(512)


def loop():
    """Main loop of the program."""
    print("loop")
    # wait until weight sensor is pressed
    while not txt.main.weight_sensor.is_closed():
        pass

    # check if there's really an object in front of the robot
    if not txt.main.front_ultrasonic.get_distance() < 20:
        return

    move_waste()
    waste = model.process_image(txt.main.camera.get_frame())

    # for each index, start a new thread to wait for the waste to pass by the phototransistor
    segregate_waste(waste)


def move_waste():
    """Move the waste to the sorting area."""
    # move forward until the object is out of range
    txt.main.front_motor.set_speed(256, Motor.CCW)
    txt.main.back_motor.set_speed(256, Motor.CCW)
    txt.main.front_motor.start_sync(txt.main.back_motor)
    while txt.main.front_ultrasonic.get_distance() < 20:
        pass
    txt.main.front_motor.stop_sync(txt.main.back_motor)


def segregate_waste(waste):
    """Segregates waste into its proper containers."""
    for i, w in enumerate(waste):
        if w["label"] == labels.BIODEGRADABLE:
            threading.Thread(target=wait_for_bio, args=(i,)).start()
        elif w["label"] == labels.CARDBOARD or w["label"] == labels.PAPER:
            threading.Thread(target=wait_for_np, args=(i,)).start()
        elif w["label"] == labels.GLASS or w["label"] == labels.METAL:
            threading.Thread(target=wait_for_rec, args=(i,)).start()
        else:  # plastic
            # wait for the waste to fall into the bin
            threading.Thread(
                target=count_pt_passes, args=(txt.ext.plastic_pt, i)
            ).start()


def wait_for_bio(count):
    """Wait for the bio waste to pass by the phototransistor."""
    count_pt_passes(txt.ext.bio_pt, count)
    use_piston(txt.main.bio_input_valve, txt.ext.bio_output_valve)


def wait_for_np(count):
    """Wait for the non-plastic waste to pass by the phototransistor."""
    count_pt_passes(txt.ext.np_pt, count)
    use_piston(txt.main.np_input_valve, txt.ext.np_output_valve)


def wait_for_rec(count):
    """Wait for the recyclable waste to pass by the phototransistor."""
    count_pt_passes(txt.ext.rec_pt, count)
    use_piston(txt.main.rec_input_valve, txt.ext.rec_output_valve)


def count_pt_passes(pt, count):
    """Count the number of times the phototransistor goes from dark to bright, i.e. an object passes by."""
    i = 0
    while i < count:
        while pt.is_dark():
            pass
        i += 1
        while pt.is_bright():
            pass


def use_piston(open_valve, close_valve):
    """Use the piston to sort the waste."""
    txt.main.back_motor.stop_sync()
    txt.main.compressor.on()
    open_valve.on()
    time.sleep(0.3)
    txt.main.compressor.off()
    open_valve.off()
    close_valve.on()
    time.sleep(0.2)
    close_valve.off()


def test_outputs():
    txt = Controller()

    print("Testing outputs...")
    txt.main.front_motor.set_speed(512)
    txt.main.back_motor.set_speed(512)
    txt.main.front_motor.start_sync(txt.main.back_motor)

    txt.main.bio_input_valve.on()
    txt.main.np_input_valve.on()
    txt.main.rec_input_valve.on()

    txt.main.compressor.on()

    txt.ext.bio_led.set_brightness(512)
    txt.ext.np_led.set_brightness(512)
    txt.ext.rec_led.set_brightness(512)

    txt.ext.bio_output_valve.on()
    txt.ext.np_output_valve.on()
    txt.ext.rec_output_valve.on()
    print("Done.")

    while True:
        pass


def test_model():
    # test the model on the camera feed
    print("Testing model...")
    while True:
        detected = model.process_image(txt.main.camera.get_frame())
        print(detected)
        time.sleep(0.5)

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
        while True:
            loop()
except Exception:
    print(traceback.format_exc())
