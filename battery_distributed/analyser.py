import os
import logging
import picamera
import numpy as np
import time

from threading import Thread, Semaphore

from battery_analyser import predict as ba_predict

LOG = "Analyser"
CAM_ID = int(os.environ.get("CAM_ID", "0"))
MAX_TRIES = int(os.environ.get("ANALYSER_MAX_TRIES", "10"))


def init() -> Semaphore:
    sem = Semaphore(value=0)
    Thread(target=run_analyser_worker, args=(sem,)).start()
    return sem


def run_analyser_worker(sem: Semaphore):
    with picamera.PiCamera() as cam:
        cam.resolution = (640, 480)
        cam.start_preview()
#        cam.color_effects=(128,128)
        output = np.empty((ba_predict.WIDTH, ba_predict.HEIGHT, 3), dtype=np.uint8)
        while True:
            time.sleep(0.5)
            for try_ in range(MAX_TRIES):
                cam.capture(output, 'rgb', resize=ba_predict.IMAGE_SIZE)
                cam.capture('imagem.jpg', resize=ba_predict.IMAGE_SIZE)

                prediction = ba_predict.predict(output)
                if not prediction:
                    if try_+1 == MAX_TRIES:
                        logging.error(f"{LOG}: max atempt reached...")
                        break
                    logging.warn(f"{LOG}: cant predict. Trying again...")
                    continue
                logging.info(f"{LOG}: {prediction}")
