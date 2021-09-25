from json import dumps

from httpx import AsyncClient

from config.main import RAPID_API_KEY


async def eight_ball_api(question: str) -> dict:
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "magic-8-ball.p.rapidapi.com",
        'x-rapidapi-key': f"{RAPID_API_KEY}"
    }

    payload = dumps({"question": f"{question}"}, separators=(',', ':'))

    async with AsyncClient(headers=headers) as client:
        r = await client.post("https://magic-8-ball.p.rapidapi.com/8-ball", data=payload)

        return r.json()
