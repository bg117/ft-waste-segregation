import numpy as np
import tensorflow as tf
from io import BytesIO
from PIL import Image


# Define image preprocessing function
def preprocess_image(frame, input_size):
    img_bytes = BytesIO(frame)
    image = Image.open(img_bytes).convert("RGB")
    image = image.resize((input_size[0], input_size[1]))
    image = np.array(image, dtype=np.float32)
    image = (image / 255.0).astype(np.float32)  # Normalize to [0,1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image


class ML:
    def __init__(self):
        # Load TFLite model and allocate tensors
        self._ip = tf.lite.Interpreter(model_path="model.tflite")
        self._ip.allocate_tensors()

        # Get input and output tensors
        self._inp_details = self._ip.get_input_details()
        self._outp_details = self._ip.get_output_details()

    # Define function to run inference
    def run_inference_for_single_image(self, frame):
        img_bytes = BytesIO(frame)

        # Preprocess image
        input_size = self._inp_details[0]["shape"][1:3]  # (height, width)
        image = preprocess_image(img_bytes, input_size)

        # Set input tensor
        self._ip.set_tensor(self._inp_details[0]["index"], image)

        # Run inference
        self._ip.invoke()

        # Get output tensor
        boxes = self._ip.get_tensor(self._outp_details[0]["index"])[0]   # Bounding boxes
        classes = self._ip.get_tensor(self._outp_details[1]["index"])[0] # Class labels
        scores = self._ip.get_tensor(self._outp_details[2]["index"])[0]  # Confidence scores

        return boxes, classes, scores
