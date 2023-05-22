import os
import asyncio
import logging

import analyser
import telemetry
import controller
from model import Maquina


async def main():
    maquina_id = os.environ.get("MAQUINA_ID", "unique id")
    maquina = Maquina(maquina_id)

    controller.init(maquina)
    analyser_sem = analyser.init()
    await telemetry.init(maquina, analyser_sem)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    asyncio.run(main())
