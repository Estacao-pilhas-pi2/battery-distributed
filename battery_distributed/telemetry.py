import logging

from threading import Semaphore
from asyncio import sleep

from model import Maquina


LOG = "Telemetry"


async def init(maquina: Maquina, analyser_sem: Semaphore):
    while True:
        analyser_sem.release()
        await sleep(30)
        logging.info(f"{LOG}: telemetry... {maquina}")
