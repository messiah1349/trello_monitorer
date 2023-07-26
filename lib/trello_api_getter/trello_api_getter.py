import requests
import json
import time
from dataclasses import dataclass, asdict
import logging
logger = logging.getLogger(__name__)


@dataclass
class TrelloBoardLists:
    backlog_id: str
    todo_id: str
    review_id: str
    done_id: str


@dataclass
class Card:
    id: str
    name: str
    due: str


cards_info_type = dict[str, dict[str, str]]

@dataclass
class TrelloCardsResponse:
    active_cards: list[cards_info_type]
    done_cards: list[cards_info_type]


class TrelloRequester:

    def __init__(self, trello_board_lists: TrelloBoardLists, api_key: str, token: str):
        self.trello_board_lists = trello_board_lists
        self.api_key = api_key
        self.token = token

    @staticmethod
    def _parse_lists_requests(response_text: str) -> list[Card]:
        return [Card(card['id'], card['name'], card['due']) for card in json.loads(response_text)]

    def _get_cards_request(self, list_id: str) -> list[Card]:
        
        url = f"https://api.trello.com/1/lists/{list_id}/cards"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        if response.status_code == 200:
            # logger.debug(f"cards for {list_id=}: {self._parse_lists_requests(response.text)}")
            return self._parse_lists_requests(response.text)
        else:
            logger.error(f"status code: {response.status_code}, text: {response.text}")
            return []

    @staticmethod
    def _merge_cards_info(*args: cards_info_type) -> cards_info_type:
        return sum([card for card in args], [])


    def get_cards(self):
        backlogs_cards = self._get_cards_request(self.trello_board_lists.backlog_id)
        todo_cards = self._get_cards_request(self.trello_board_lists.todo_id)
        review_cards = self._get_cards_request(self.trello_board_lists.review_id)
        done_cards = self._get_cards_request(self.trello_board_lists.done_id)

        active_cards = self._merge_cards_info(backlogs_cards, todo_cards, review_cards)

        cards_response = TrelloCardsResponse(active_cards, done_cards)

        return cards_response


class TrelloCardsChangeMonitorer(TrelloRequester):
    def __init__(self, 
                    trello_board_lists: TrelloBoardLists, 
                    api_key: str, 
                    token: str,
                    scheduler_host: str,
                    scheduler_port: str):
                    
        super().__init__(trello_board_lists, api_key, token)
        self.card_due_stance = {} #cards_info_type
        self.scheduler_host = scheduler_host
        self.scheduler_port = scheduler_port

    def _send_request(self, card: Card, route: str, method: str, data: dict):
        url = f'{self.scheduler_host}:{self.scheduler_port}{route}'
        response = requests.request(method=method, url=url, json=data)
        return response

    def _send_new_due_request(self, card: Card):
        response = self._send_request(card, '/api/v1/add_task/', 
                                      'POST', asdict(card))
        logger.debug(f'send {card=}, {response.text=}')

    def _delete_active_card_request(self, card: Card):
        response = self._send_request(card, '/api/v1/delete_task/',
                                    'DELETE', asdict(card))
        logger.debug(f'delete {card=}, {response.text=}')

    def _proceed_active_exist_card(self, card: Card) -> None:
        stance_due = self.card_due_stance[card.id]['due']
        if stance_due != card.due:
            self.card_due_stance[card.id]['due'] = card.due
            self._send_new_due_request(card)

    def _proceed_new_active_card(self, card: Card) -> None:
        self.card_due_stance[card.id] = {'name': card.name, 'due': card.due}
        if card.due is not None:
            self._send_new_due_request(card)

    def _proceed_done_exist_card(self, card: Card) -> None:
        del self.card_due_stance[card.id]
        if card.due is not None:
            self._delete_active_card_request(card)

    def _get_update(self):

        cards = self.get_cards()
        for card in cards.active_cards:
            if card.id in self.card_due_stance: #new due in old card
                self._proceed_active_exist_card(card)
            else:
                self._proceed_new_active_card(card) #new card

        for card in cards.done_cards:
            if card.id in self.card_due_stance:
                self._proceed_done_exist_card(card) #new card in done
            else:
                pass

    def build(self):
        while True:
            # print('startanuli!')
            # logger.debug(f"{self.card_due_stance=}")
            self._get_update()
            time.sleep(5)

    