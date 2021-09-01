from decouple import config

# Get configuration from env.

token = config('API_TOKEN')
bot_prefix = config('PREFIX')
owner_id = eval(config('OWNER_ID'))
crown_role_id: int = eval(config('BLACK_HOLE_ID'))
color = eval(config('COLOR'))
tenor_key = config('TENOR_API_KEY')
