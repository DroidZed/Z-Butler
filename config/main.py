from decouple import config

# Get configuration from env.

token = config('API_TOKEN')
prefix = config('PREFIX')
owner_id = eval(config('OWNER_ID'))
crown_role_id = eval(config('BLACK_HOLE_ID'))
color = eval(config('COLOR'))
