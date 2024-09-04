import controller

US_THRESHOLD = 15

def loop(txt: controller.TXTController):
    # wait until the weight sensor is triggered
    while txt.weight_sensor.state() == 0:
        pass

    # check if there is really an object or if it was a false positive
    if txt.ultrasonic.front.distance() > 20:
        return
    
    # run the preface and main motors
    txt.encoder.preface.setSpeed(512)
    txt.encoder.main.setSpeed(512)

    # wait until less than US_THRESHOLD
    while txt.ultrasonic.object_confirm.distance() > US_THRESHOLD:
        pass

    # stop the preface and main motors
    txt.encoder.preface.setSpeed(0)
    txt.encoder.main.setSpeed(0)

# --- essentials ---

def main(txt: controller.TXTController):
    txt.camera.start()

    while True:
        loop(txt)

def test_controls(txt: controller.TXTController):
    txt.solenoid.bio.open()
    txt.solenoid.nc.open()
    txt.solenoid.rec.open()

    txt.compressor.setLevel(512) # turn on compressor
    
    txt.encoder.preface.setSpeed(512) # start preface motor
    txt.encoder.main.setSpeed(512) # start main motor

    w = txt.weight_sensor.state() # read weight sensor
    u1 = txt.ultrasonic.front.distance() # read front ultrasonic sensor
    u2 = txt.ultrasonic.bio.distance() # read bio ultrasonic sensor
    u3 = txt.ultrasonic.np.distance() # read np ultrasonic sensor
    u4 = txt.ultrasonic.rec.distance() # read rec ultrasonic sensor

    print(f'PB Trigger: {w}, Front: {u1} cm, Bio: {u2} cm, NP: {u3} cm, Rec: {u4} cm')