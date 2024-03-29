import os
import time
import logging
import serial

from threading import Thread
from subprocess import Popen, PIPE
from typing import Optional

from battery_analyser.predict import Battery
from battery_distributed.model import Machine, MachineSession, MACHINE_SESSION_MAX_INACTIVE_SECS
import battery_distributed.analyser as analyser
import battery_distributed.central as central
import battery_distributed.interface as interface


LOG = "Controller"
SERIAL_PORT = os.environ.get("SERIAL_PORT", "/dev/ttyUSB0")
BAUDRATE = os.environ.get("BAUDRATE", 19200)
SERIAL = None

machine_session: MachineSession = None
current_timer = 0


def init(machine: Machine):
    Thread(target=controller_spawner, args=(machine,)).start()
    Thread(target=timer).start()


def controller_spawner(machine: Machine):
    while True:
        try:
#            logging.info(f"{LOG}: Connecting {SERIAL_PORT} serial port")
            with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
                SERIAL = ser
                ser.reset_input_buffer()
                ser.reset_output_buffer()

                line = ser.readline()
                if not line:
                    continue
                response = run_command(machine, line)

                if response:
                    logging.info(f"{LOG}: sending response: {response}")
                    ser.write(response.encode('utf-8'))
                    ser.flush()
        except KeyboardInterrupt:
            return
        except Exception as e:
            if SERIAL is not None:
                SERIAL.close()
            logging.error(f"{LOG}: Error in serial port. Reconnecting in 5 seconds... {e}")

        time.sleep(5)


LOCKER_OPEN = b"G0"
LOCKER_CLOSED = b"G1"
AAA_EMPTY = b"AAA0"
AAA_NEMPTY = b"AAA1"
AA_EMPTY = b"AA0"
AA_NEMPTY = b"AA1"
V9_EMPTY = b"9V0"
V9_NEMPTY = b"9V1"
C_EMPTY = b"C0"
C_NEMPTY = b"C1"
D_EMPTY = b"D0"
D_NEMPTY = b"D1"
IMAGE_ANALYSE = b"AI"


def run_command(machine: Machine, command: bytes) -> Optional[str]:
    global current_timer

    logging.info(f"{LOG}: received command: {command}")

    if command[:len(IMAGE_ANALYSE)] == IMAGE_ANALYSE:
        interface.change_to_processing()
        reset_machine_session_countdown(machine)
        type = analyser.predict_battery_type()
        increment_battery(machine, type)
        increment_battery(machine_session, type)
        if type == Battery.UNKNOWN:
            current_timer = 0
            interface.change_to_session_error()
            current_timer = 5
        else:
            interface.add_session_state(machine_session)
            interface.set_countdown(machine_session.inactive_countdown)
            current_timer = 1
        return f"AI{type.value}"

    if command[:len(V9_EMPTY)] == V9_EMPTY:
        machine.v9_count = 0
        central.send_machine_empty(machine, "V9")

    if command[:len(AA_EMPTY)] == AA_EMPTY:
        machine.aa_count = 0
        central.send_machine_empty(machine, "AA")

    if command[:len(AAA_EMPTY)] == AAA_EMPTY:
        machine.aaa_count = 0
        central.send_machine_empty(machine, "AAA")

    if command[:len(C_EMPTY)] == C_EMPTY:
        machine.c_count = 0
        central.send_machine_empty(machine, "C")

    if command[:len(D_EMPTY)] == D_EMPTY:
        machine.d_count = 0
        central.send_machine_empty(machine, "D")


def increment_battery(machine: Machine, battery: Battery):
    if battery == Battery.V9:
        machine.v9_count += 1
    elif battery == Battery.AA:
        machine.aa_count += 1
    elif battery == Battery.AAA:
        machine.aaa_count += 1
    elif battery == Battery.D:
        machine.d_count += 1
    elif battery == Battery.C:
        machine.c_count += 1


def create_machine_session(machine: Machine):
    global machine_session
    machine_session = MachineSession(id=machine.id)
    logging.info(f"{LOG}: creating machine session. Countdown = {machine_session.inactive_countdown}")
    interface.add_session_state(machine_session)

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
            response = central.send_payment(machine_session)
            interface.change_to_session_end(machine_session, response)
            machine_session = None
            current_timer = 30
            logging.info(f"{LOG}: ending machine session")
            continue
        
        machine_session.inactive_countdown -= 1
        logging.info(f"{LOG}: decrementing machine session. Countdown = {machine_session.inactive_countdown}")
        interface.set_countdown(machine_session.inactive_countdown)
        logging.info(f"{LOG}: end set countdown")
        current_timer = 1
    
