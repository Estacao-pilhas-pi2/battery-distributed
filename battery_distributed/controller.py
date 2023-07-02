import os
import time
import logging
import signal

from threading import Thread
from subprocess import Popen, PIPE
from typing import Optional

from battery_analyser.predict import Battery
from battery_distributed.model import Machine, MachineSession, MACHINE_SESSION_MAX_INACTIVE_SECS
import battery_distributed.analyser as analyser
import battery_distributed.central as central
import battery_distributed.interface as interface


LOG = "Controller"
CONTROLLER_RUNNER = os.environ.get("CONTROLLER_RUNNER_PATH", "python3 tests/controller_mock.py")
PROCESS = None

machine_session: MachineSession = None
current_timer = 0


def init(machine: Machine):
    Thread(target=controller_spawner, args=(machine,)).start()
    Thread(target=timer).start()


def controller_spawner(machine: Machine):
    while True:
        try:
            logging.info(f"{LOG}: Spawning {CONTROLLER_RUNNER} controller")
            with Popen(CONTROLLER_RUNNER.split(), stdout=PIPE, stdin=PIPE, text=True) as proc:
                PROCESS = proc
                for line in proc.stdout:
                    if not line:
                        continue
                    line = line.strip()
                    if not line:
                        continue
                    response = run_command(machine, line)
                    
                    if response:
                        logging.info(f"{LOG}: sending response: {response}")
                        proc.stdin.write(response)
                        proc.stdin.write("\n")
                        proc.stdin.flush()
        except Exception as e:
            if PROCESS is not None:
                PROCESS.terminate()
            logging.error(f"{LOG}: Error in controller runner. Respawnning in 5 seconds... {e}")

        time.sleep(5)


LOCKER_OPEN = "G0"
LOCKER_CLOSED = "G1"
AAA_EMPTY = "AAA0"
AAA_NEMPTY = "AAA1"
AA_EMPTY = "AA0"
AA_NEMPTY = "AA1"
V9_EMPTY = "9V0"
V9_NEMPTY = "9V1"
C_EMPTY = "C0"
C_NEMPTY = "C1"
D_EMPTY = "D0"
D_NEMPTY = "D1"
IMAGE_ANALYSE = "AI"


def run_command(machine: Machine, command: str) -> Optional[str]:
    global current_timer

    logging.info(f"{LOG}: received command: {command}")

    if command == IMAGE_ANALYSE:
        interface.change_to_processing()
        reset_machine_session_countdown(machine)
        type = analyser.predict_battery_type()
        increment_battery(machine, type)
        increment_battery(machine_session, type)
        if type == Battery.UNKNOWN:
            current_timer = 0
            interface.change_to_session_error()
            current_timer = 10
        else:
            interface.add_session_state(machine_session)
            interface.set_countdown(machine_session.inactive_countdown)
            current_timer = 1
        return f"AI{type.value}"

    if command == V9_EMPTY:
        machine.v9_count = 0
        central.send_machine_empty(machine)

    if command == AA_EMPTY:
        machine.aa_count = 0
        central.send_machine_empty(machine)

    if command == AAA_EMPTY:
        machine.aaa_count = 0
        central.send_machine_empty(machine)

    if command == C_EMPTY:
        machine.c_count = 0
        central.send_machine_empty(machine)

    if command == D_EMPTY:
        machine.d_count = 0
        central.send_machine_empty(machine)


def increment_battery(machine: Machine, battery: Battery):
    if battery == Battery.V9:
        machine.v9_count += 1
    elif battery == Battery.AA:
        machine.aa_count += 1
    elif battery == Battery.AAA:
        machine.aaa_count += 1
    elif battery == Battery.D:
        machine.d_count += 1
    # elif battery == Battery.C:
    #   machine.quantidade_C += 1


def create_machine_session(machine: Machine):
    global machine_session
    machine_session = MachineSession(id=machine.id)
    logging.info(f"{LOG}: creating machine session. Countdown = {machine_session.inactive_countdown}")


def reset_machine_session_countdown(machine: Machine):
    global current_timer
    current_timer = 0
    if not machine_session:
        create_machine_session(machine)
    machine_session.inactive_countdown = MACHINE_SESSION_MAX_INACTIVE_SECS


def timer():
    global machine_session, current_timer

    while True:
        time.sleep(1)

        if current_timer > 0:
            current_timer = current_timer - 1
            continue


        if not machine_session:
            interface.change_to_main_screen()
            continue

        if machine_session.inactive_countdown == 0:
            central.send_payment(machine_session)
            interface.change_to_session_end(machine_session)
            machine_session = None
            current_timer = 30
            logging.info(f"{LOG}: ending machine session")
            continue
        
        machine_session.inactive_countdown -= 1
        logging.info(f"{LOG}: decrementing machine session. Countdown = {machine_session.inactive_countdown}")
        interface.set_countdown(machine_session.inactive_countdown)
        logging.info(f"{LOG}: end set countdown")
        current_timer = 1
    