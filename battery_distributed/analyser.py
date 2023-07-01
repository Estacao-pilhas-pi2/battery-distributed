import os
import logging
# import picamera
import random
import numpy as np

from battery_analyser import predict as ba_predict

LOG = "Analyser"
CAM_ID = int(os.environ.get("CAM_ID", "0"))
MAX_TRIES = int(os.environ.get("ANALYSER_MAX_TRIES", "10"))
MAX_UNKNOWN_TRIES = int(os.environ.get("ANALYSER_MAX_UNKNOWN_TRIES", 2))


def predict_battery_type() -> ba_predict.Battery:
    return ba_predict.Battery(random.randint(0, 4))

    with picamera.PiCamera() as cam:
        cam.resolution = (640, 480)
        cam.start_preview()
        output = np.empty((ba_predict.WIDTH, ba_predict.HEIGHT, 3), dtype=np.uint8)

        for try_ in range(MAX_TRIES):
            cam.capture(output, "rgb", resize=ba_predict.IMAGE_SIZE)
            # cam.capture('imagem.jpg', resize=ba_predict.IMAGE_SIZE)

            prediction = ba_predict.predict(output)
            if not prediction:
                if try_ + 1 == MAX_TRIES:
                    logging.error(f"{LOG}: max atempt reached...")
                    break
                logging.warn(f"{LOG}: cant predict. Trying again...")
                continue
            if prediction == ba_predict.Battery.UNKNOWN and try_ + 1 < MAX_UNKNOWN_TRIES:
                continue
            logging.info(f"{LOG}: {prediction}")
            return prediction
