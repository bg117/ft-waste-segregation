import cv2
import numpy as np

from .Detector import Detector


class ImageClassifier(Detector):

    def process_image(self, image):
        
        result = []
        if image is None:
            return result
        
        orig_width = image.shape[1]
        orig_height = image.shape[0]

        input_details = self.interpreter.get_input_details()
        input_shape = input_details[0]['shape']
        height = input_shape[1]
        width = input_shape[2]

        image = cv2.resize(image, (width, height))
        input_data = np.expand_dims(image, axis=0)  # expand to 4-dim

        # analyse image
        self.interpreter.set_tensor(self.interpreter.get_input_details()[0]['index'], input_data)
        self.interpreter.invoke()

        # result of the analysis
        output_details = self.interpreter.get_output_details()
        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        output_data = np.squeeze(output_data)

        k = 1 # only the first result is relevant
        sorted_output = output_data.argsort()[-k:][::-1]
        for _id in sorted_output:
            score = float(output_data[_id] / 255.0)
            if score > 0.5:
                result.append({
                    'label': self.labels[_id],
                    'position': [0, 0, orig_width, orig_height],
                    'probability': score
                })

        return result
