from lib.trello_api_getter import TrelloCardsChangeMonitorer, TrelloBoardLists
from secret import *

board_list = TrelloBoardLists(lists[0][0], lists[1][0], lists[2][0], lists[3][0])
monitorer = TrelloCardsChangeMonitorer(board_list, api_key, token)
monitorer.build()