import requests
import apsw
import re


sql = apsw.Connection("pogo/data/pkmn.db")

cursor = sql.cursor()
for version, in cursor.execute("SELECT value FROM settings WHERE key = 'game_master'"):
    r = requests.get("https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest-version.txt")
    if version >= r.text:
        sql.close()
        exit(0)

r = requests.get("https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest/V2_GAME_MASTER.json")
master = r.json()

repkmn = re.compile('^[V][0-9]\S+(_POKEMON_)')

for entry in master['template']:
    if repkmn.match(entry['templateId']):
        print(entry['templateId'])

sql.close()