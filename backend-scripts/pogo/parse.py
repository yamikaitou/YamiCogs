import requests
import json
import re
import os


os.chdir(os.path.dirname(__file__))
if os.path.exists("../../pogo/data/pkmn.json"):
    os.remove("../../pogo/data/pkmn.json")
    with open("../../pogo/data/pkmn.json", "w") as f:
        json.dump({"version":"0"}, f)
with open("../../pogo/data/pkmn.json") as f:
    data = json.load(f)

r = requests.get("https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest-version.txt")
if data['version'] >= r.text:
    exit(0)

r = requests.get("https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest/V2_GAME_MASTER.json")
master = r.json()

repkmn = re.compile('^(FORMS_)[V][0-9]\S+(_POKEMON_)')

for entry in master['template']:
    if repkmn.match(entry['templateId']):
        print(entry['data']['formSettings']['pokemon'])
