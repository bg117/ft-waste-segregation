import cv2
import imutils
import numpy as np
import colorsys

from ..models.Ball import Ball
from .Detector import Detector
from .DetectorResult import DetectorResult


class BallDetector(Detector):

    def __init__(self, x, y, width, height, min_ball_diameter=5, max_ball_diameter=20, start_range_value=-100, end_range_value=100, rgb=[255,0,0], hue_tolerance=20, identifier="ball_detector"):
        Detector.__init__(self, identifier)
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__min_ball_diameter = min_ball_diameter
        self.__max_ball_diameter = max_ball_diameter
        self.__start_x_range_value = start_range_value
        self.__end_x_range_value = end_range_value
        self.__start_y_range_value = int(height / width * start_range_value)
        self.__end_y_range_value = int(height / width * end_range_value)
        # Creates lower (dark) / upper (light) hsv color from given rgb color.
        # Divide tolerance by 4, because opencv works with a hue range of 0-180, 
        # but the given tolerance is based on a range of 0-360.
        self.__lower_color = self.__create_hsv_limit(rgb, hue_tolerance / 4, -1)
        self.__upper_color = self.__create_hsv_limit(rgb, hue_tolerance / 4)
    
    def analyze_frame(self, frame):

        # crop image
        crop_img = frame[self.__y:self.__y + self.__height, self.__x:self.__x + self.__width]
        
        # resize the frame, blur it, and convert it to the HSV
        # color space
        blurred = cv2.GaussianBlur(crop_img, (11, 11), 0)      
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.__lower_color, self.__upper_color)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        
        # only proceed if at least one contour was found
        ball = None
        if len(contours) > 0:
            # find the largest contour in the mask
            contour = max(contours, key=cv2.contourArea)
            (orig_x, orig_y), orig_radius = cv2.minEnclosingCircle(contour)

            # transform x, y, radius to the given range
            abs_x_range = abs(self.__end_x_range_value - self.__start_x_range_value)  
            abs_y_range = abs(self.__end_y_range_value - self.__start_y_range_value)  

            x = ((orig_x * abs_x_range) / self.__width) + self.__start_x_range_value 
            y = ((orig_y * abs_y_range) / self.__height) + self.__start_y_range_value
            radius = abs_x_range / self.__width * orig_radius
            diameter = radius * 2

            if diameter >= self.__min_ball_diameter and diameter <= self.__max_ball_diameter:
                ball = Ball(
                    int(x),
                    int(y),
                    int(radius), 
                    int(orig_x), 
                    int(orig_y),
                    int(orig_radius)
                )

        self.__ball = ball

        # executes callbacks when detection is successful
        if self.detected():
            for callback in self._callbacks:
                callback(self.get_result())
            

    def draw_contour(self, frame):
        if self.detected() == True:
            color = (0,255,0)
            thickness = 2
            x = self.__x + self.__ball.orig_x
            y = self.__y + self.__ball.orig_y
            radius = self.__ball.orig_radius - 2 * thickness
            if radius > 0:
                cv2.circle(frame, (x, y), radius, color, thickness)

    def get_result(self):
        return DetectorResult(self._identifier, self.detected(), self.__ball)

    def get_center_x(self):
        if self.__ball is not None:
            return self.__ball.x
        return None

    def get_center_y(self):
        if self.__ball is not None:
            return self.__ball.y
        return None

    def get_radius(self):
        if self.__ball is not None:
            return self.__ball.radius
        return None

    def get_diameter(self):
        if self.__ball is not None:
            return self.__ball.diameter
        return None

    def detected(self):
        if self.__ball is not None:
            return True
        return False

    def __create_hsv_limit(self, rgb, hue_tolerance, upper_or_lower=1):
        # convert rgb to hsv color space
        h, s, v = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
        # convert to opencv hsv color space
        h = int(h * 180)
        s = int(s * 255)
        v = int(v * 255)
        # adjust hue, saturation, value
        h = self.__adjust_value(h, hue_tolerance * upper_or_lower, 180)
        s = self.__adjust_value(s, 64 * upper_or_lower, 255)
        v = self.__adjust_value(v, 64 * upper_or_lower, 255)
        return (h, s, v)

    # adjust value via tolerance and boundary
    def __adjust_value(self, value, tolerance, boundary):
        value = value + tolerance
        if value > boundary:
            value = boundary
        elif value < 0:
            value = 0
        return value
