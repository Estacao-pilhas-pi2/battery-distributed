import os
import time
import random
import logging

from threading import Thread, Semaphore
from subprocess import Popen, PIPE

from battery_distributed.model import Maquina

LOG = "Controller"
CONTROLLER_RUNNER_PATH=os.environ.get("CONTROLLER_RUNNER_PATH", "tests/controller_mock.sh")


def init(maquina: Maquina, analyser_sem: Semaphore):
    Thread(target=controller_spawner, args=(maquina, analyser_sem)).start()


def controller_spawner(maquina: Maquina, analyser_sem: Semaphore):
    while True:
        try:
            logging.info(f"{LOG}: Spawning {CONTROLLER_RUNNER_PATH} controller")
            with Popen([CONTROLLER_RUNNER_PATH], stdout=PIPE, stdin=PIPE) as proc:
                for line in proc.stdout:
                    logging.debug(f"{LOG}: Receiving from controller: {line}")
                    # Mock
                    analyser_sem.release()
                    maquina.quantidade_AA = random.randint(0, 20)
                    maquina.quantidade_AAA = random.randint(0, 20)
                    maquina.quantidade_C = random.randint(0, 20)
                    maquina.quantidade_D = random.randint(0, 20)
                    maquina.quantidade_V9 = random.randint(0, 20)

        except Exception as e:
            logging.error(f"{LOG}: Error in controller runner. Respawnning in 5 seconds... {e}")
            time.sleep(5)
