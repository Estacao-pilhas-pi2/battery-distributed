import logging
from . import main, controller

try:
    logging.getLogger().setLevel(logging.INFO)
    main.main()
except:
    if controller.SERIAL is not None:
        controller.SERIAL.close()
