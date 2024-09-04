import controller

def test_controls(txt: controller.TXTController):
    txt.solenoid.bio.open()
    txt.solenoid.nc.open()
    txt.solenoid.rec.open()

    txt.compressor.setLevel(512) # turn on compressor
    
    txt.encoder.preface.setSpeed(512) # start preface motor
    txt.encoder.main.setSpeed(512) # start main motor

def main(txt: controller.TXTController):
    pass