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


def init(machine: Machine):
    signal.signal(signal.SIGALRM, end_machine_session)
    Thread(target=controller_spawner, args=(machine,)).start()


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
    logging.info(f"{LOG}: received command: {command}")

    if command == IMAGE_ANALYSE:
        reset_machine_session_countdown(machine)
        type = analyser.predict_battery_type()
        increment_battery(machine, type)
        increment_battery(machine_session, type)
        if type == Battery.UNKNOWN:
            # TODO: show error in display
            ...
        else:
            # TODO: increment display battery counts...
            ...
        start_countdown()
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
    signal.alarm(0)
    if not machine_session:
        create_machine_session(machine)
    machine_session.inactive_countdown = MACHINE_SESSION_MAX_INACTIVE_SECS
    interface.set_countdown(machine_session.inactive_countdown)


def end_machine_session(signum, frame):
    global machine_session

    if not machine_session:
        return

    if machine_session.inactive_countdown == 0:
        central.send_payment(machine_session)
        machine_session = None
        signal.alarm(0)
        logging.info(f"{LOG}: ending machine session")
        return
    
    machine_session.inactive_countdown -= 1
    interface.set_countdown(machine_session.inactive_countdown)
    signal.alarm(1)
    logging.info(f"{LOG}: decrementing machine session. Countdown = {machine_session.inactive_countdown}")


def start_countdown():
    signal.alarm(1)
