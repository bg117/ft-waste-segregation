import cv2
import numpy as np

from .Detector import Detector


class ObjectDetector(Detector):

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
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(image, axis=0)  # expand to 4-dim

        # analyse image
        self.interpreter.set_tensor(self.interpreter.get_input_details()[0]['index'], input_data)
        self.interpreter.invoke()

        # result of the analysis
        output_details = self.interpreter.get_output_details()
        # output_details[0] - position
        # output_details[1] - class id
        # output_details[2] - score
        # output_details[3] - count

        positions = np.squeeze(self.interpreter.get_tensor(output_details[0]['index']))
        classes = np.squeeze(self.interpreter.get_tensor(output_details[1]['index']))
        scores = np.squeeze(self.interpreter.get_tensor(output_details[2]['index']))

        for idx, score in enumerate(scores):
            if score > 0.5:
                x1 = int(max(0, positions[idx][1] * orig_width))
                x2 = int(min(positions[idx][3] * orig_width, orig_width))
                y1 = int(max(0, positions[idx][0] * orig_height))
                y2 = int(min(positions[idx][2] * orig_height, orig_height))
                result.append({
                    'label': self.labels[int(classes[idx])],
                    'position': [x1, y1, x2, y2],
                    'probability': score
                })

        return sorted(result, key=lambda i: i['probability'], reverse=True)

