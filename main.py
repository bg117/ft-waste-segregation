import controller
import program

# connect to the TXT controller
txt = controller.TXTController()
test_controls = False

if test_controls:
    txt.run(program.test_controls)
else:
    txt.run(program.main)