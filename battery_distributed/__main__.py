import logging
import asyncio
from . import main, controller

try:
    logging.getLogger().setLevel(logging.DEBUG)
    asyncio.run(main.main())
except:
    if controller.PROCESS is not None:
        controller.PROCESS.terminate()
