import base64
import multiprocessing

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite


class Detector(object):

    interpreter = None
    labels = []

    def __init__(self, model_path, label_path):
        self.interpreter = self.load_model(model_path)
        self.labels = self.load_labels(label_path)

    def load_labels(self, label_path):
        r"""Returns a list of labels"""
        with open(label_path) as f:
            labels = {}
            index = 0
            for line in f.readlines():
                labels[index] = line.rstrip('\n')
                index = index + 1
            return labels

    def load_model(self, model_path):
        r"""Load TFLite model, returns a Interpreter instance."""
        core_count = multiprocessing.cpu_count()
        interpreter = tflite.Interpreter(model_path=model_path, num_threads=core_count)
        interpreter.allocate_tensors()
        return interpreter

    def process_image(self, image):
        pass


    def process_base64_image(self, encoded_image):
        decoded_data = base64.b64decode(encoded_image)
        np_array = np.frombuffer(decoded_data, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
        return self.process_image(image)