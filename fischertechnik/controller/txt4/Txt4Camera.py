import base64
import threading
import time
from types import SimpleNamespace

import cv2

from ..Camera import Camera
from ...camera.VideoStream import VideoStream


class Txt4Camera(Camera):

    def __init__(self, controller, identifier):
        Camera.__init__(self, controller, identifier)
        self.__lock = threading.Lock()
        self.__debug = False
        self.__frame = None
        self.__thread = None
        self.__running = False
        self.__callbacks = []
        self.__detectors = []
        self.__blocked_areas = []
        self.__output = []

    def __del__(self):
        self.stop()
        
    def start(self, **kwargs):
        
        for key, value in kwargs.items():
            if key == 'width':
                VideoStream.getInstance().set_width(value)
            if key == 'height':
                VideoStream.getInstance().set_height(value)
            if key == 'fps':
                VideoStream.getInstance().set_fps(value)
            if key == 'rotate':
                VideoStream.getInstance().set_rotate(value)
            if key == 'debug':
                self.__debug = value
        
        VideoStream.getInstance().start()
        if VideoStream.getInstance().is_running() == False:
            return

        if self.__running == True:
            return
           
        self.__running = True
        self.__thread = threading.Thread(target=self.__update, args=(), daemon=True)
        self.__thread.start()
        
    def stop(self):
        self.__running = False
        if self.__thread is not None:
            self.__thread.join()
        VideoStream.getInstance().stop()

    def is_running(self):
        return self.__running

    def read(self):
        with self.__lock:
            output = self.__output
            success = self.__success
            if self.__frame is not None:
                frame = self.__frame.copy()
            else:
                output = None
                success = False
                frame = None
        return success, frame, output

    def add_detector(self, detector):
        with self.__lock:
            self.__detectors.append(detector)

    def add_blocked_area(self, rectangle):
        with self.__lock:
            self.__blocked_areas.append(rectangle)

    def clear_detectors(self):
        with self.__lock:
            self.__detectors.clear()

    def clear_blocked_areas(self):
        with self.__lock:
            self.__blocked_areas.clear()

    def has_frame(self):
        return self.__frame is not None

    def read_frame(self):
        if not self.is_running():
            raise Exception('Camera is not running')
        while not self.has_frame():
            time.sleep(0.1)
        return self.__frame

    def set_fps(self, fps):
        VideoStream.getInstance().set_fps(fps)

    def set_width(self, width):
        VideoStream.getInstance().set_width(width)

    def set_height(self, height):
        VideoStream.getInstance().set_height(height)

    def set_rotate(self, rotate):
        VideoStream.getInstance().set_rotate(rotate)

    def set_debug(self, debug):
        self.__debug = debug

    def get_image(self):
        if self.__frame is not None:
            return self.__frame
        return None    

    def get_image_base64(self, quality=100):
        if self.__frame is not None:
            return Txt4Camera.frame_to_base64(self.__frame.copy(), quality)
        return None

    def __update(self):
        while self.__running == True:
            output = []
            success, orig_frame = VideoStream.getInstance().read()

            if success:  
                frame = orig_frame.copy()

                # inform the listener that a new image is available
                if len(self.__callbacks) > 0:
                    image = frame.copy()
                    for callback in self.__callbacks:
                        callback(
                            SimpleNamespace(
                                identifier='image',
                                value=image
                            )
                        )

                # colorize blocked areas white for frame analyzing
                for blocked_area in self.__blocked_areas:
                    x1 = blocked_area.x
                    y1 = blocked_area.y
                    x2 = x1 + blocked_area.width
                    y2 = y1 + blocked_area.height
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), -1) 

                # analyze the frame
                for detector in self.__detectors:
                    detector.analyze_frame(frame)
                    if self.__debug:
                        detector.draw_contour(orig_frame)
                        output.append(detector.get_result().to_dict())

            with self.__lock:
                self.__frame = orig_frame
                self.__success = success
                self.__output = output

            time.sleep(1 / VideoStream.getInstance().get_fps())
                
    @staticmethod
    def frame_to_jpg(frame, quality=100):
        success, image = cv2.imencode('.jpeg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        if success:
            return image
        return None

    @staticmethod
    def frame_to_base64(frame, quality=100):
        image = Txt4Camera.frame_to_jpg(frame, quality)
        if image is not None:
            return 'data:image/jpeg;base64,' + base64.b64encode(image).decode('utf-8')
        return None

    def add_change_listener(self, property_name, callback):
        if property_name != 'image':
            raise NotImplementedError
        if callback not in self.__callbacks:
            self.__callbacks.append(callback)
        
    def remove_change_listener(self, property_name, callback):
        if property_name != 'image':
            raise NotImplementedError
        if callback in self.__callbacks:
            self.__callbacks.remove(callback)
