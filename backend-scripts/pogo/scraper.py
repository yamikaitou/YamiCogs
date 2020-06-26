import bs4
import aiohttp
import asyncio
from io import BytesIO

from bs4 import BeautifulSoup
import html5lib
import os
import requests
import re
import json

URL = "https://pokemondb.net/pokedex/all"
os.chdir(os.path.dirname(__file__))

# DOESNT DO MEGAS ETC.


async def main():
    a = {"mega": [], "normal": []}
    r = requests.get(URL)
    parse = BeautifulSoup(r.text, "html5lib")
    await asyncio.sleep(3)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    da = soup.find_all("table", {"id": "pokedex"})[0]
    tags = da.find_all("tr")
    stat_headlines = ["HP", "Attack", "Defence", "Sp. Atk", "Sp. Def", "Speed"]
    for i, poke in enumerate(tags[1:]):
        name = poke.find("a")
        _id = poke.find("span", {"class": "infocard-cell-data"}).get_text()
        small = poke.find("small", {"class": "text-muted"})
        name = name.get_text() if name is not None else f"Undefined-{i}"
        if small is not None:
            small = small.get_text()
        else:
            small = None
        reform = re.compile("(Mega|Alolan|Galarian|Partner)")
        if small != None:
            if not reform.match(small):
                a["normal"].append(
                    {
                        "name": name,
                        "alias": small,
                        "id": _id,
                    }
                )
        else:
            a["normal"].append(
                {
                    "name": name,
                    "alias": small,
                    "id": _id,
                }
            )
    await write(a)


async def write(lst):
    with open("pokemon.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(lst, indent=2))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())