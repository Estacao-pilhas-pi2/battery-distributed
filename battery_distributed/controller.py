import os
import time
import logging

from model import Maquina
from threading import Thread
from subprocess import Popen, PIPE

LOG = "Controller"
CONTROLLER_RUNNER_PATH=os.environ.get("CONTROLLER_RUNNER_PATH", "tests/controller_mock.sh")


def init(maquina: Maquina):
    Thread(target=controller_spawner).start()


def controller_spawner():
    while True:
        try:
            logging.info(f"{LOG}: Spawning {CONTROLLER_RUNNER_PATH} controller")
            with Popen([CONTROLLER_RUNNER_PATH], stdout=PIPE, stdin=PIPE) as proc:
                for line in proc.stdout:
                    logging.debug(f"{LOG}: Receiving from controller: {line}")

        except Exception as e:
            logging.error(f"{LOG}: Error in controller runner. Respawnning in 5 seconds... {e}")
            time.sleep(5)
