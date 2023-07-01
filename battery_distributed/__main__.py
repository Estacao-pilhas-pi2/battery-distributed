import logging
from . import main, controller

try:
    logging.getLogger().setLevel(logging.DEBUG)
    main.main()
except:
    if controller.PROCESS is not None:
        controller.PROCESS.terminate()
