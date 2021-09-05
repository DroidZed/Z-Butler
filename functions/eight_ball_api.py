from httpx import AsyncClient
from config.main import RAPID_API_KEY
from json import dumps


async def eight_ball_api(question: str) -> dict:
    url = "https://magic-8-ball.p.rapidapi.com/8-ball"

    payload = dumps(
        {"question": f"{question}"}, separators=(',', ':'))

    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "magic-8-ball.p.rapidapi.com",
        'x-rapidapi-key': f"{RAPID_API_KEY}"
    }

    async with AsyncClient(headers=headers) as client:
        r = await client.post(url, data=payload)

        return r.json()
