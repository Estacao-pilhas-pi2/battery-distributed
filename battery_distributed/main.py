import os
import time
import battery_distributed.central as central
import battery_distributed.controller as controller
from battery_distributed.model import Machine


def main():
    maquina_id = os.environ.get("MAQUINA_ID", "unique id")
    maquina = Machine(maquina_id)

    controller.init(maquina)
    # gui.init()

    # TODO: remove this later
    while True:
        time.sleep(10)