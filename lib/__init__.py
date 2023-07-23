import logging
import datetime
from lib.trello_api_getter import TrelloCardsChangeMonitorer, TrelloBoardLists
from lib.common.constants import (TASK_SCHEDULER_HOST,
                                    TASK_SCHEDULER_PORT,
                                    API_KEY,
                                    TOKEN, 
                                    lists
                                )

# clear handlers
root_logger = logging.root
root_logger.handlers.clear()

# init module logger
root_module_logger = logging.getLogger(__name__)
root_module_logger.setLevel(logging.DEBUG)

# format
formatter = logging.Formatter(
    '%(asctime)s - [%(name)s: %(levelname)s] - %(message)s'
)
logging.Formatter.formatTime = (
	lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created)
)

# add stdout handler
# stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler = logging.FileHandler('stdout_notify_bot_log.txt', mode='w')
stdout_handler.addFilter(lambda entry: entry.levelno <= logging.INFO)
stdout_handler.setFormatter(formatter)
root_module_logger.addHandler(stdout_handler)

stderr_handler = logging.FileHandler('stderr_notify_bot_log.txt', mode='w')
stderr_handler.addFilter(lambda entry: entry.levelno > logging.INFO)
stderr_handler.setFormatter(formatter)
root_module_logger.addHandler(stderr_handler)

root_module_logger.info("Logging was inited")


board_list = TrelloBoardLists(lists[0][0], lists[1][0], lists[2][0], lists[3][0])
monitorer = TrelloCardsChangeMonitorer(board_list, API_KEY, TOKEN, TASK_SCHEDULER_HOST, TASK_SCHEDULER_PORT)