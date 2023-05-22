import os
import cv2
import logging

from threading import Thread, Semaphore

from battery_analyser import predict as ba_predict

LOG = "Analyser"
CAM_ID = int(os.environ.get("CAM_ID", "0"))


def init() -> Semaphore:
    sem = Semaphore(value=0)
    Thread(target=run_analyser_worker, args=(sem,)).start()
    return sem


def run_analyser_worker(sem: Semaphore):
    cam = cv2.VideoCapture(CAM_ID)

    while True:
        sem.acquire()
        _, frame = cam.read()

        frame = cv2.resize(frame, ba_predict.IMAGE_SIZE)
        prediction = ba_predict.predict(frame)
        logging.info(f"{LOG}: {prediction}")
