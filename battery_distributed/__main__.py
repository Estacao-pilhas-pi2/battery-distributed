import logging
import asyncio
from . import main

logging.getLogger().setLevel(logging.DEBUG)
asyncio.run(main.main())
