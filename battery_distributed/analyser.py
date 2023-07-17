import os
import io
import logging
import picamera
import random
import time
import numpy as np
from PIL import Image
from battery_analyser import predict as ba_predict

LOG = "Analyser"
CAM_ID = int(os.environ.get("CAM_ID", "0"))
MAX_TRIES = int(os.environ.get("ANALYSER_MAX_TRIES", "3"))
START_DELAY = float(os.getenv("START_DELAY", "0.2"))

def predict_battery_type() -> ba_predict.Battery:
#    return ba_predict.Battery(random.randint(0, 4))
#    breakpoint()
    time.sleep(START_DELAY)
    predictions = [0, 0, 0, 0, 0, 0, 0]
    with picamera.PiCamera() as cam:
        cam.resolution = (640, 480)
        cam.start_preview()

        for try_ in range(MAX_TRIES):
            stream = io.BytesIO()
            cam.capture(stream, format="jpeg")
            image = Image.open(stream).crop((0,60, 430, 420))

            image.save("image.jpg")
            image = image.resize(ba_predict.IMAGE_SIZE)
            prediction = ba_predict.predict(np.array(image))
            Image.fromarray(np.array(image)).save("teste.jpg")
            if prediction == ba_predict.Battery.UNKNOWN:
                predictions[ba_predict.Battery.UNKNOWN.value] += 1
                continue
            logging.info(f"{LOG}: {prediction}")
            predictions[prediction.value] += 1
#            return prediction
        index = 0

        for i in range(1, len(predictions)):
            if predictions[i] >= predictions[index]:
                index = i
        logging.info(f"{LOG}: {predictions}")
        return ba_predict.Battery(index)

if __name__ == "__main__":
    import time
    logging.getLogger().setLevel(logging.INFO)
    while True:
        print(predict_battery_type(), "-" * 100)
        time.sleep(1)
