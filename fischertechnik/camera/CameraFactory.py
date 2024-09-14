from ..models.Rectangle import Rectangle
from .BallDetector import BallDetector
from .ColorDetector import ColorDetector
from .LineDetector import LineDetector
from .MotionDetector import MotionDetector


class CameraFactory():
    
    def create_line_detector(self, x, y, width, height, min_line_width=5, max_line_width=20, start_range_value=-100, end_range_value=100, number_of_lines=1, invert=False):
        """@ReturnType fischertechnik.camera.LineDetector"""
        return LineDetector(x, y, width, height, min_line_width, max_line_width, start_range_value, end_range_value, number_of_lines, invert)

    def create_ball_detector(self, x, y, width, height, min_ball_diameter=5, max_ball_diameter=20, start_range_value=-100, end_range_value=100, rgb=[255,0,0], hue_tolerance=20):
        """@ReturnType fischertechnik.camera.BallDetector"""
        return BallDetector(x, y, width, height, min_ball_diameter, max_ball_diameter, start_range_value, end_range_value, rgb, hue_tolerance)

    def create_color_detector(self, x, y, width, height, contrast=1.0):
        """@ReturnType fischertechnik.camera.ColorDetector"""
        return ColorDetector(x, y, width, height, contrast)
    
    def create_motion_detector(self, x, y, width, height, tolerance=1.0):
        """@ReturnType fischertechnik.camera.MotionDetector"""
        return MotionDetector(x, y, width, height, tolerance)

    def create_blocked_area(self, x, y, width, height):
        """@ReturnType fischertechnik.camera.Rectangle"""
        return Rectangle(x, y, width, height)
