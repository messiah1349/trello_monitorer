import os
from lib.trello_api_getter import TrelloCardsChangeMonitorer, TrelloBoardLists

lists = [['648ff8b8470180a3a7c4995d', 'backlog'],
 ['648ff8bb624e117850aa5a52', 'to do'],
 ['648ff8c336033571473c832f', 'review'],
 ['648ff8c5c041fe27d955184c', 'done']]

API_KEY = os.getenv('TRELLO_API')
TOKEN = os.getenv('TRELLO_TOKEN')

board_list = TrelloBoardLists(lists[0][0], lists[1][0], lists[2][0], lists[3][0])
monitorer = TrelloCardsChangeMonitorer(board_list, API_KEY, TOKEN)
monitorer.build()