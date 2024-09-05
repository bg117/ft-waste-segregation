import controller
import program
import ml

# connect to the TXT controller
txt = controller.TXTController()
test_controls = False

od = ml.ML()

if test_controls:
    txt.run(program.test_controls, od)
else:
    txt.run(program.main, od)
