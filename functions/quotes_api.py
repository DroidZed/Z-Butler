from typing import Dict

from config.main import RAPID_API_KEY
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from httpx import AsyncClient


async def quotes_gql() -> Dict:

    transport = AIOHTTPTransport(
        url="https://spark-api-graphql.herokuapp.com/")

    async with Client(transport=transport, fetch_schema_from_transport=True,) as session:

        query = gql(
            """
        query {
            randomQuote {
                author
                body
            }
        }
    """)

        return await session.execute(query)


async def quotes_rest() -> dict:

    headers = {
        'x-rapidapi-host': "quotes15.p.rapidapi.com",
        'x-rapidapi-key': f"{RAPID_API_KEY}"
    }

    async with AsyncClient(headers=headers) as client:

        r = await client.get("https://quotes15.p.rapidapi.com/quotes/random/")

        return r.json()