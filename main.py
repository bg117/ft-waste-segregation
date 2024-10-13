import time
import traceback
import cv2
import numpy
import base64
import requests

from fischertechnik.controller.Motor import Motor
from lib.controller import Controller

# Global Variables and Initialization
txt = None  # type: Controller

upload_url = "https://detect.roboflow.com/trash-detection-kfzaq/10?api_key=HXC352N4WELuCWfPDA8M&format=json&stroke=5"


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


def process_waste_item():
    """Main loop to process each waste item."""
    frame = txt.main.camera.read_frame()
    ret, buffer = cv2.imencode('.jpg', frame)
    img_str = base64.b64encode(buffer)

    # Get prediction from Roboflow Infer API
    response = requests.post(upload_url, data=img_str, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }).json()

    prediction = response['predictions'][0]
    label = prediction['class']

    if label == "cardboard" or label == "paper":
        handle_np_waste()
    elif label == "glass" or label == "metal":
        handle_recyclable_waste()
    elif label == "plastic":
        handle_plastic_waste()
    elif label == "organic waste":
        handle_bio_waste()


def move_waste_to_sorting_area():
    """Moves waste to the sorting area."""
    txt.ext.front_motor.set_speed(300, Motor.CCW)
    txt.ext.back_motor.set_speed(200, Motor.CCW)
    txt.ext.front_motor.start()
    txt.ext.back_motor.start()


def handle_bio_waste():
    """Handles bio-waste sorting."""
    wait_for_phototransistor(txt.main.bio_pt)
    activate_sorting_piston(txt.main.bio_valve)


def handle_np_waste():
    """Handles non-plastic waste sorting."""
    wait_for_phototransistor(txt.main.np_pt)
    activate_sorting_piston(txt.main.np_valve)


def handle_recyclable_waste():
    """Handles recyclable waste sorting."""
    wait_for_phototransistor(txt.main.rec_pt)
    activate_sorting_piston(txt.main.rec_valve)


def handle_plastic_waste():
    """Handles plastic waste sorting."""
    wait_for_phototransistor(txt.main.rec_pt)
    time.sleep(1)


def activate_sorting_piston(valve):
    """Activates the piston to sort the waste."""
    time.sleep(0.82)

    txt.ext.back_motor.stop()
    txt.ext.front_motor.stop()

    valve.on()
    time.sleep(0.75)
    valve.off()

    move_waste_to_sorting_area()


def main():
    """Main entry point of the program."""
    initialize_controller()

    configure_robot()
    move_waste_to_sorting_area()

    while True:
        process_waste_item()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
