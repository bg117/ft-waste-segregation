import cv2

from ..models.Color import Color
from .Detector import Detector
from .DetectorResult import DetectorResult


class ColorDetector(Detector):

    def __init__(self, x, y, width, height, contrast=1.0, identifier="color_detector"):
        Detector.__init__(self, identifier)
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__contrast = contrast
        self.__color = None

    def analyze_frame(self, frame):
        
        crop_img = frame[self.__y:self.__y + self.__height, self.__x:self.__x + self.__width]
        hsvImg = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
        # decreasing the contrast 0.0 - 1.0
        hsvImg[..., 2] = hsvImg[..., 2] * self.__contrast
        image = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2RGB)        
        mean = image.mean(axis=0).mean(axis=0)
        
        if mean is not None:
            self.__color = Color(rgb=[int(mean[0]), int(mean[1]), int(mean[2])])
        else:
            self.__color = None

        # executes callbacks when detection is successful
        if self.detected():
            for callback in self._callbacks:
                callback(self.get_result())

    def get_result(self):
        return DetectorResult(self._identifier, self.detected(), self.__color)

    def get_color(self, format="RGB"):
        if self.__color is not None:
            if format == "RGB":
                return self.__color.rgb
            elif format == "HEX":
                return self.__color.hex
        return None

    def compare_color(self, color=[0,0,0], tolerance=1.0, format="RGB"):
        if self.__color is not None:
            return self.__color.compare(color, tolerance, format)
        return False

    def detected(self):
        if self.__color is not None:
            return True
        return False