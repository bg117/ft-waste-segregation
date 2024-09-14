from apds9960.const import *
from apds9960 import APDS9960
from smbus import SMBus

import threading
import time

from ...models.Color import Color
from ..GestureSensor import GestureSensor

class Txt4GestureSensor(GestureSensor):

    def __init__(self, controller, identifier):
        GestureSensor.__init__(self, controller, identifier)
        self.__apds = APDS9960(SMBus(3))
        self.__lock = threading.Lock()
        self.__thread = None
        self.__gesture = APDS9960_DIR_NONE
        self.__last_gesture_time = time.time()

    def enable_light(self):
        self.__stop_read_gesture()
        self.__apds.enableLightSensor()

    def disable_light(self):
        self.__apds.disableLightSensor()

    def get_ambient(self):
        return self.__apds.readAmbientLight()

    def get_color(self):
        return Color(rgb=[
            self.__apds.readRedLight(),
            self.__apds.readGreenLight(),
            self.__apds.readBlueLight()
        ])

    def get_rgb_red(self):
        return self.get_color().get_rgb_red()

    def get_rgb_green(self):
        return self.get_color().get_rgb_green()

    def get_rgb_blue(self):
        return self.get_color().get_rgb_blue()

    def get_rgb(self):
        return self.get_color().get_rgb()

    def get_hsv_hue(self):
        return self.get_color().get_hsv_hue()

    def get_hsv_saturation(self):
        return self.get_color().get_hsv_saturation()

    def get_hsv_value(self):
        return self.get_color().get_hsv_value()

    def get_hsv(self):
        return self.get_color().get_hsv()

    def get_hex(self):
        return self.get_color().get_hex()

    def enable_proximity(self, threshold = 50):
        self.__stop_read_gesture()
        self.__apds.setProximityIntLowThreshold(threshold)
        self.__apds.enableProximitySensor()

    def disable_proximity(self):
        self.__apds.disableProximitySensor()

    def get_proximity(self):
        return self.__apds.readProximity()

    def enable_gesture(self, threshold = 50):
        self.__apds.setProximityIntLowThreshold(threshold)
        self.__apds.enableGestureSensor()
        self.__start_read_gesture()

    def disable_gesture(self):
        self.__stop_read_gesture()
        self.__apds.disableGestureSensor()

    def get_gesture(self):
        return self.__gesture

    def __start_read_gesture(self):
        self.__stop_read_gesture()
        self.__running = True
        self.__thread = threading.Thread(target=self.__read_gesture, args=(), daemon=True)
        self.__thread.start()
    
    def __stop_read_gesture(self):
        self.__running = False
        if self.__thread is not None:
            self.__thread.join()
            self.__thread = None

    def __read_gesture(self):
        while self.__running:
            if self.__apds.isGestureAvailable():
                with self.__lock:
                    self.__gesture = self.__apds.readGesture()
                    self.__last_gesture_time = time.time()
            else:
                current_time = time.time()
                if (current_time - self.__last_gesture_time) > 0.7:
                    with self.__lock:
                        self.__gesture = APDS9960_DIR_NONE

