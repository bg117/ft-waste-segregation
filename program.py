import controller

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

def main(txt: controller.TXTController):
    pass