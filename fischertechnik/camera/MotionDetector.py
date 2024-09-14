import cv2
import imutils

from .Detector import Detector
from .DetectorResult import DetectorResult


class MotionDetector(Detector):

    MIN_AREA = 500
    GAUSSIAN_KERNEL_SIZE = 21

    def __init__(self, x, y, width, height, tolerance=1.0, identifier="motion_detector"):
        Detector.__init__(self, identifier)
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__tolerance = tolerance
        self.__detected = False
        self.__prev_gray = None

    def analyze_frame(self, frame):

        crop_img = frame[self.__y:self.__y + self.__height, self.__x:self.__x + self.__width]
        gray = self.__gray_scale_frame(crop_img)
        
        if self.__prev_gray is None:
            self.__prev_gray = gray
            return

        diff = cv2.absdiff(self.__prev_gray, gray)
        self.__prev_gray = gray

        threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)
        
        cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        min_area = self.MIN_AREA * self.__tolerance
        detected = False
        for c in cnts:
            if cv2.contourArea(c) > min_area:
                detected = True
                break
        
        self.__detected = detected

        # executes callbacks when detection is successful
        if self.detected():
            for callback in self._callbacks:
                callback(self.get_result())

    def draw_contour(self, frame):
        if self.detected() == True:
            # create a copy of the original
            overlay = frame.copy()
            # draw shape
            color = (0,255,0)
            cv2.rectangle(
                overlay,
                (self.__x, self.__y),
                (self.__x + self.__width, self.__y + self.__height),
                color,
                -1
            )
            # blend with the original
            opacity = 0.5
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

    def __gray_scale_frame(self, frame):
        return cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                                (self.GAUSSIAN_KERNEL_SIZE, self.GAUSSIAN_KERNEL_SIZE), 0)

    def get_result(self):
        return DetectorResult(self._identifier, self.detected())

    def detected(self):
        return self.__detected