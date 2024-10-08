import fischertechnik.factories as txt_factory

txt_factory.init()
txt_factory.init_input_factory()
txt_factory.init_output_factory()
txt_factory.init_motor_factory()
txt_factory.init_usb_factory()
txt_factory.init_camera_factory()


class MainController:
    def __init__(self):
        self._txt = txt_factory.controller_factory.create_graphical_controller()

        self.push_button = txt_factory.input_factory.create_mini_switch(self._txt, 1)
        self.front_ultrasonic = (
            txt_factory.input_factory.create_ultrasonic_distance_meter(self._txt, 2)
        )

        self.front_pt = txt_factory.input_factory.create_photo_transistor(self._txt, 7)

        self.bio_pt = txt_factory.input_factory.create_photo_transistor(self._txt, 3)
        self.np_pt = txt_factory.input_factory.create_photo_transistor(self._txt, 4)
        self.rec_pt = txt_factory.input_factory.create_photo_transistor(self._txt, 5)

        self.bio_valve = txt_factory.output_factory.create_magnetic_valve(self._txt, 5)
        self.np_valve = txt_factory.output_factory.create_magnetic_valve(self._txt, 6)
        self.rec_valve = txt_factory.output_factory.create_magnetic_valve(self._txt, 7)

        self.compressor = txt_factory.output_factory.create_compressor(self._txt, 1)

        self.camera = txt_factory.usb_factory.create_camera(self._txt, 1)

        cam = self.camera
        cam.set_rotate(False)
        cam.set_height(240)
        cam.set_width(320)
        cam.set_fps(15)
        # cam.start()


class ExtController:
    def __init__(self):
        self._txt = txt_factory.controller_factory.create_graphical_controller(2)

        self.front_motor = txt_factory.motor_factory.create_encodermotor(self._txt, 1)
        self.back_motor = txt_factory.motor_factory.create_encodermotor(self._txt, 2)

        self.bio_led = txt_factory.output_factory.create_led(self._txt, 5)
        self.np_led = txt_factory.output_factory.create_led(self._txt, 6)
        self.rec_led = txt_factory.output_factory.create_led(self._txt, 7)


class Controller:
    def __init__(self):
        txt_factory.init()
        txt_factory.init_input_factory()
        txt_factory.init_output_factory()
        txt_factory.init_motor_factory()
        txt_factory.init_usb_factory()
        txt_factory.init_camera_factory()

        self.main = MainController()
        self.ext = ExtController()

        txt_factory.initialized()
