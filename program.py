import time
import controller
from controller import BIO, NP, REC, pwm

US_THRESHOLD = 15

txt: controller.TXTController

def loop():
    # wait until the weight sensor is triggered
    while txt.weight_sensor.state() == 0:
        pass

    # check if there is really an object or if it was a false positive
    if txt.ultrasonic.front.distance() > 20:
        return
    
    # run the preface and main motors
    move_waste()

    array = detect_waste()
    segregate_waste(array)

def segregate_waste(array):
    while len(array) > 0:
        type = array.pop()
        # run the main motor and wait until the corresponding ultrasonic sensor detects the object
        txt.encoder.main.setSpeed(512)

        while txt.ultrasonic[type].distance() > US_THRESHOLD:
            pass

        # stop the main motor and push the bio waste
        txt.encoder.main.setSpeed(0)

        txt.solenoid[type].open()
        txt.compressor.setLevel(pwm(True))
        # wait 1 second
        time.sleep(1)

        # close the solenoid and turn off the compressor
        txt.compressor.setLevel(pwm(False))
        txt.solenoid[type].close()

def move_waste():
    txt.encoder.preface.setSpeed(512)
    txt.encoder.main.setSpeed(512)

    # wait until less than US_THRESHOLD
    while txt.ultrasonic.object_confirm.distance() > US_THRESHOLD:
        pass

    # stop the preface and main motors
    txt.encoder.preface.setSpeed(0)
    txt.encoder.main.setSpeed(0)

def detect_waste():
    # array of bio, np, and rec types detected in the frame (from right to left)
    return []

# --- essentials ---

def main(ct: controller.TXTController):
    txt = ct

    txt.camera.start()

    while True:
        loop()

def test_controls(ct: controller.TXTController):
    ct.solenoid[BIO].open()
    ct.solenoid[NP].open()
    ct.solenoid[REC].open()

    ct.compressor.setLevel(512) # turn on compressor
    
    ct.encoder.preface.setSpeed(512) # start preface motor
    ct.encoder.main.setSpeed(512) # start main motor

    w = ct.weight_sensor.state() # read weight sensor
    u1 = ct.ultrasonic.front.distance() # read front ultrasonic sensor
    u2 = ct.ultrasonic[BIO].distance() # read bio ultrasonic sensor
    u3 = ct.ultrasonic[NP].distance() # read np ultrasonic sensor
    u4 = ct.ultrasonic[REC].distance() # read rec ultrasonic sensor

    print(f'PB Trigger: {w}, Front: {u1} cm, Bio: {u2} cm, NP: {u3} cm, Rec: {u4} cm')