import cv2
import numpy as np
import colorsys

class Color(object):
    
    def __init__(self, **kwargs):
        
        if "rgb" in kwargs:
            self.__rgb = kwargs["rgb"]
        elif "hsv" in kwargs:
            self.__rgb = self.__hsv2rgb(kwargs["hsv"])
        elif "hex" in kwargs:
            self.__rgb = self.__hex2rgb(kwargs["hex"])
        else:
            raise Exception("unknow color type")

    def to_json(self):
        return {
            'rgb' : self.get_rgb(),
            'hsv' : self.get_hsv(),
            'hex' : self.get_hex()
        }

    def get_rgb_red(self):
        rgb = self.get_rgb()
        return rgb[0]

    def get_rgb_green(self):
        rgb = self.get_rgb()
        return rgb[1]

    def get_rgb_blue(self):
        rgb = self.get_rgb()
        return rgb[2]

    def get_rgb(self):
        return self.__rgb

    def get_hsv_hue(self):
        hsv = self.get_hsv()
        return hsv[0]

    def get_hsv_saturation(self):
        hsv = self.get_hsv()
        return hsv[1]

    def get_hsv_value(self):
        hsv = self.get_hsv()
        return hsv[2]

    def get_hsv(self):
        rgb = self.get_rgb()
        return self.__rgb2hsv(rgb)

    def get_hex(self):
        rgb = self.get_rgb()
        return self.__rgb2hex(rgb)

    def compare(self, **kwargs):

        if "rgb" in kwargs:
            hsv = self.__rgb2hsv(kwargs["rgb"])
        elif "hsv" in kwargs:
            hsv = kwargs["hsv"]
        elif "hex" in kwargs:
            hsv = self.__hex2hsv(kwargs["hex"])
        else:
            raise Exception("unknow color type")

        hue_tolerance = 20
        if "hue_tolerance" in kwargs:
            hue_tolerance = kwargs["hue_tolerance"]

        lower = self.__create_hsv_limit(self.get_hsv(), hue_tolerance / 2, -1)    
        upper = self.__create_hsv_limit(self.get_hsv(), hue_tolerance / 2)    

        if int(hsv[0]) in range(lower[0], upper[0]) and int(hsv[1]) in range(lower[1], upper[1]) and int(hsv[2]) in range(lower[2], upper[2]):
            return True

        return False

    def __hex2rgb(self, hex_str):
        hex_str = hex_str.lstrip('#')
        hlen = len(hex_str)
        return list(tuple(int(hex_str[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3)))

    def __rgb2hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    def __rgb2hsv(self, rgb):
        h, s, v = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
        return [int(h * 360), int(s * 100), int(v * 100)]

    def __hsv2rgb(self, hsv):
        r, g, b = colorsys.hsv_to_rgb(hsv[0] / 360, hsv[1] / 100, hsv[2] / 100)
        return [int(r * 255), int(g * 255), int(b * 255)]

    def __hex2hsv(self, hex_str):
        rgb = self.__hex2rgb(hex_str)
        return self.__rgb2hsv(rgb)

    def __hsv2hex(self, hsv):
        rgb = self.__hsv2rgb(hsv)
        return self.__rgb2hex(rgb)

    def __create_hsv_limit(self, hsv, hue_tolerance, upper_or_lower=1):
        # adjust hue, saturation, value
        h = self.__adjust_value(hsv[0], hue_tolerance * upper_or_lower, 360)
        s = self.__adjust_value(hsv[1], 25 * upper_or_lower, 100)
        v = self.__adjust_value(hsv[2], 25 * upper_or_lower, 100)
        return [int(h), int(s), int(v)]

    # adjust value via tolerance and boundary
    def __adjust_value(self, value, tolerance, boundary):
        value = value + tolerance
        if value > boundary:
            value = boundary
        elif value < 0:
            value = 0
        return value
