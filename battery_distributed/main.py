import os
import asyncio
import logging

import battery_distributed.analyser as analyser
import battery_distributed.telemetry as telemetry
import battery_distributed.controller as controller
from battery_distributed.model import Maquina


async def main():
    maquina_id = os.environ.get("MAQUINA_ID", "unique id")
    maquina = Maquina(maquina_id)

    controller.init(maquina)
    analyser_sem = analyser.init()
    await telemetry.init(maquina, analyser_sem)
