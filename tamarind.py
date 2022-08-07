""" heartbreak already hit me once so swear that it won't happen twice """

import logging
import logging.config
from app import TamarindTuiApp


def tamarind_thread():
    """ Start the game """
    logging.basicConfig(level=logging.INFO, filename="tamarind.log",
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('tamarind')
    # init main thread
    logger.info('starting main thread')
    # init tui app
    logger.info('starting tui app')
    tui_app = TamarindTuiApp(logger)
    tui_app.run()
    logger.info('finished tui app')
    # wait for next run

    logger.info('finished main thread')

if __name__ == '__main__':
    tamarind_thread()
