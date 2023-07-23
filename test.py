import os
from lib import monitorer
from secret import api_key, token

monitorer.token = token
monitorer.api_key = api_key
monitorer.build()