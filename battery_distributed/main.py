import os
import time
import signal

import battery_distributed.central as central
import battery_distributed.interface as interface
import battery_distributed.controller as controller
from battery_distributed.model import Machine

def terminate(signum, frame):
    print("Finalizando lindamente...")
    if controller.PROCESS is not None:
        controller.PROCESS.terminate()
    interace.APP.quit()

def main():
    maquina_id = os.environ.get("MAQUINA_ID", "1")
    maquina = Machine(maquina_id)

    controller.init(maquina)
    interface.run()
