from decouple import config

# Get configuration from env.

TOKEN = config('API_TOKEN')
PREFIX = config('PREFIX')
OWNER_ID = eval(config('OWNER_ID'))
CROWN_ROLE_ID: int = eval(config('BLACK_HOLE_ID'))
COLOR = eval(config('COLOR'))
TENOR_KEY = config('TENOR_API_KEY')
RAPID_API_KEY = config('RAPID_API_KEY')
