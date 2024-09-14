import sys
import threading
import time


import cv2
import imutils
import numpy


class VideoStream(object):
    __MAX_RETRY = 10
    __instance = None

    __thread = None
    __frame = None
    __success = False

    __rotate = False
    __width = 320
    __height = 240
    __fps = 15

    @staticmethod
    def getInstance():
        """ Static access method. """
        if VideoStream.__instance == None:
            VideoStream()
        return VideoStream.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if VideoStream.__instance != None:
            raise Exception("This class is a Singleton!")
        else:
            numpy.set_printoptions(threshold=sys.maxsize)
            VideoStream.__instance = self
            self.__lock = threading.Lock()
            self.__running = False
            self.__video_capture = cv2.VideoCapture(0)

    def __del__(self):
        self.stop()

    def start(self):

        for _ in range(self.__MAX_RETRY):
            if self.__video_capture.isOpened() == False:
                self.__video_capture = cv2.VideoCapture(0)
                time.sleep(1)
            else:
                break

        if self.__video_capture.isOpened() == False:
            return

        self.__video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__height)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.__width)
        self.__video_capture.set(cv2.CAP_PROP_FPS, self.__fps)

        if self.__running == True:
            return

        self.__running = True
        self.__thread = threading.Thread(target=self.__update, args=(), daemon=True)
        self.__thread.start()

    def stop(self):
        self.__running = False
        if self.__thread is not None:
            self.__thread.join()
        if self.__video_capture is not None:
            self.__video_capture.release()

    def is_running(self):
        return self.__running

    def read(self):
        with self.__lock:
            success = self.__success
            if self.__frame is not None:
                frame = self.__frame.copy()
            else:
                success = False
                frame = None
        return success, frame

    def set_fps(self, fps):
        if fps is not None:
            self.__fps = fps

    def get_fps(self):
        return self.__fps

    def set_width(self, width):
        if width is not None:
            self.__width = width

    def get_width(self):
        return self.__width

    def set_height(self, height):
        if height is not None:
            self.__height = height

    def get_height(self):
        return self.__height

    def set_rotate(self, rotate):
        if rotate is not None:
            self.__rotate = rotate

    def __update(self):
        while self.__running == True:
            success, frame = self.__video_capture.read()
            with self.__lock:
                self.__success = success
                frame = imutils.resize(frame, width=self.__width, height=self.__height)
                if self.__rotate:
                    self.__frame = cv2.rotate(frame, cv2.ROTATE_180)
                else:
                    self.__frame = frame
            time.sleep(1 / self.__fps)
