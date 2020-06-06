import requests
import zipfile
import os

os.chdir(os.path.dirname(__file__))
if os.path.exists("server.jar"):
    os.remove("server.jar")

r = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
versions = r.json()
version = versions['latest']['release']
url = None
for urls in versions['versions']:
    if urls['id'] == version:
        url = urls['url']
        break

r = requests.get(url)
jar = r.json()['downloads']['server']['url']

r = requests.get(jar, allow_redirects=True)
open('server.jar', 'wb').write(r.content)

with zipfile.ZipFile("server.jar") as z:
    z.extract("assets\minecraft\lang\en_us.json")