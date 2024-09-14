import cv2
import imutils
import numpy as np

from ..models.Line import Line
from ..models.Color import Color
from .Detector import Detector
from .DetectorResult import DetectorResult

class LineDetector(Detector):

    def __init__(self, x, y, width, height, min_line_width=5, max_line_width=20, start_range_value=-100, end_range_value=100, number_of_lines=1, invert=False, identifier="line_detector"):
        Detector.__init__(self, identifier)
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__min_line_width = min_line_width
        self.__max_line_width = max_line_width
        self.__start_range_value = start_range_value
        self.__end_range_value = end_range_value
        self.__number_of_lines = number_of_lines
        self.__invert = invert
        self.__lines = None

    def analyze_frame(self, frame):

        # crop image
        crop = frame[self.__y:self.__y + self.__height, self.__x:self.__x + self.__width]

        # convert to grayscale
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # if invert True, white lines are detected
        if self.__invert == True:
            gray = cv2.bitwise_not(gray)

        # blurred image
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # create a binary thresholded image
        _, binary = cv2.threshold(blur, 127,255, cv2.THRESH_BINARY_INV)

        # find the contours of the frame
        contours = []
        if imutils.is_cv3():
            _, contours, _ = cv2.findContours(binary, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # find the most promising candidates
        candidates = []
        for contour in contours:
 
            # approximate the contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

            # if the shape has 4 vertices, it is either a square or
		    # a rectangle
            if len(approx) == 4:
                candidates.append(contour)

        # get the 5 largest contours
        lines = []
        for contour in candidates:

            # dimension of the line
            orig_x, orig_y, orig_width, orig_height = cv2.boundingRect(contour)

            # Mass center of the line
            M = cv2.moments(contour)
            if M['m00'] == 0:
                continue

            # transform position and line width to the given range
            width = orig_width
            orig_range = self.__width
            orig_position = int(M['m10'] / M['m00'])
            if self.__height > self.__width:
                # vertical alignment of the line detection,
                # use y for evaluation
                width = orig_height
                orig_range = self.__height
                orig_position = int(M['m01'] / M['m00'])

            abs_range = abs(self.__start_range_value - self.__end_range_value) 
            position = ((orig_position * abs_range) / orig_range) + self.__start_range_value
            width = abs_range / orig_range * width

            if width < self.__min_line_width or width > self.__max_line_width:
                break

            # average color of the line
            mask = np.zeros(crop.shape[:2], np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, -1)
            mask = cv2.erode(mask, None, iterations=2)
            # FT-6868 RPC 6.1.5: Rot und Blau beim Linienfeld vertauscht
            # [:3] entfernen, dreht das Array um
            mean = cv2.mean(crop, mask=mask)[:3]
            color = Color(rgb=[int(mean[0]), int(mean[1]), int(mean[2])])
            
            line = Line(
                int(position),
                int(width), 
                color, 
                int(orig_x),
                int(orig_y), 
                int(orig_width),
                int(orig_height)
            )
            lines.append(line)  
    
        if self.__height > self.__width:
            # sort from top to bottom
            lines.sort(key=lambda line: line.orig_y, reverse=False)
        else:
            # sort from left to right
            lines.sort(key=lambda line: line.orig_x, reverse=False)

        if (len(lines) > 0):
            # copy the first n lines
            self.__lines = lines[:self.__number_of_lines]
        else:
            self.__lines = None

        # executes callbacks when detection is successful
        if self.detected():
            for callback in self._callbacks:
                callback(self.get_result())
                
    def draw_contour(self, frame):
        if self.detected() == True:
            # create a copy of the original
            overlay = frame.copy()
            # draw shapes
            color = (0,255,0)
            for i in range(len(self.__lines)):
                line = self.__lines[i]
                x1 = self.__x + line.orig_x
                y1 = self.__y + line.orig_y
                x2 = x1 + line.orig_width
                y2 = y1 + line.orig_height
                cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
            # blend with the original
            opacity = 0.5
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
            # draw numbers
            color = (255,255,255)
            thickness = 2
            for i in range(len(self.__lines)):
                line = self.__lines[i]
                x1 = self.__x + line.orig_x
                y1 = self.__y + line.orig_y
                x2 = x1 + line.orig_width
                y2 = y1 + line.orig_height
                cv2.putText(frame, str(i+1), (x1 + 4, y1 + 16), cv2.FONT_HERSHEY_SIMPLEX , 0.5, color, thickness)


    def get_result(self):
        return DetectorResult(self._identifier, self.detected(), self.__lines)

    def get_width_by_index(self, index):
        line = self.get_line_by_index(index)
        if line is not None:
            return line.width
        return None

    def get_position_by_index(self, index):
        line = self.get_line_by_index(index)
        if line is not None:
            return line.position
        return None

    def get_color_by_index(self, index, format='RGB'):
        line = self.get_line_by_index(index)
        if line is not None:
            if format == "RGB":
                return line.color.rgb
            elif format == "HEX":
                return line.color.hex
        return None

    def compare_color_by_index(self, index, color=[0,0,0], tolerance=1.0, format='RGB'):
        line = self.get_line_by_index(index)
        if line is not None:
            return line.color.compare(color, tolerance, format)
        return False

    def get_line_by_index(self, index):
        if self.__lines is not None and len(self.__lines) > index:
            return self.__lines[index]
        return None

    def get_line_count(self):
        if self.__lines is not None:
            return len(self.__lines)
        return 0

    def detected(self):
        if self.__lines is not None:
            return True
        return False