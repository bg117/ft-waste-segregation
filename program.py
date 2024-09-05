import time
import controller
from controller import BIO, NP, REC, PLASTIC, pwm
import ml

US_THRESHOLD = 15

txt: controller.TXTController
od: ml.ML


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

        if type == PLASTIC:
            # wait until the plastic ultrasonic sensor detects the object
            while txt.ultrasonic[PLASTIC].distance() > US_THRESHOLD:
                pass

            # wait one second to let the object fall into the bin
            time.sleep(1)

            # next loop
            continue

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
    # get camera frame
    frame = txt.camera.frame()
    boxes, classes, _ = od.run_inference_for_single_image(frame)

    # sort classes by boxes[i][3] (right to left)
    # for each class, group each number into either BIO, NP, REC, or PLASTIC
    classes_sorted = [
        c[1] for c in sorted(zip(boxes, classes), key=lambda x: x[0][3], reverse=True)
    ]
    classes_selected = [group_class(c) for c in classes_sorted]

    # array of bio, np, and rec types detected in the frame (from right to left)
    return classes_selected


def group_class(c: int):
    # if c is in 0, BIO; 1-5 NP; 6-10 REC; 11-15 PLASTIC
    if c == 0:
        return BIO
    if c in range(1, 6):
        return NP
    if c in range(6, 11):
        return REC
    if c in range(11, 16):
        return PLASTIC


# --- essentials ---


def main(ct: controller.TXTController, ml: ml.ML):
    global txt, od

    txt = ct
    od = ml

    txt.camera.start()

    while True:
        loop()


def test_controls(ct: controller.TXTController):
    ct.solenoid[BIO].open()
    ct.solenoid[NP].open()
    ct.solenoid[REC].open()

    ct.compressor.setLevel(512)  # turn on compressor

    ct.encoder.preface.setSpeed(512)  # start preface motor
    ct.encoder.main.setSpeed(512)  # start main motor

    w = ct.weight_sensor.state()  # read weight sensor
    u1 = ct.ultrasonic.front.distance()  # read front ultrasonic sensor
    u2 = ct.ultrasonic[BIO].distance()  # read bio ultrasonic sensor
    u3 = ct.ultrasonic[NP].distance()  # read np ultrasonic sensor
    u4 = ct.ultrasonic[REC].distance()  # read rec ultrasonic sensor
    u5 = ct.ultrasonic[PLASTIC].distance()
    u6 = ct.ultrasonic.object_confirm.distance()

    print(
        f"PB Trigger: {w}, Front: {u1} cm, Bio: {u2} cm, NP: {u3} cm, Rec: {u4} cm, Plastic: {u5}, Object Confirmation: {u6}"
    )
