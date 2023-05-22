import logging

from threading import Semaphore
from asyncio import sleep

from battery_distributed.model import Maquina


LOG = "Telemetry"


async def init(maquina: Maquina, analyser_sem: Semaphore):
    while True:
        analyser_sem.release()
        await sleep(5)
        logging.info(f"{LOG}: telemetry... {maquina}")
