import os
import httpx
import logging

from asyncio import sleep
from dataclasses import asdict
from threading import Semaphore

from battery_distributed.model import Maquina


LOG = "Telemetry"
DELAY_SECONDS = int(os.environ.get("TELEMETRY_DELAY_SECONDS", "5"))
SERVER_API_TOKEN = os.environ.get("TELEMETRY_API_TOKEN", "")
SERVER_HOST = os.environ.get("TELEMETRY_SERVER_HOST", "http://localhost:8000")
SERVER_BASE_URL = f"{SERVER_HOST}/api/maquina"


async def init(maquina: Maquina):
    client = httpx.AsyncClient(base_url=SERVER_BASE_URL)

    while True:
        await sleep(DELAY_SECONDS)
        logging.info(f"{LOG}: sending telemetry... {maquina}")
        # await send_telemetry(client, maquina)


async def send_telemetry(client: httpx.AsyncClient, maquina: Maquina):
    await client.post(f"{maquina.id}/telemetry", json=asdict(maquina))
