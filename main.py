import logging
import os
import re
import shutil

from rich.logging import RichHandler

with open("EmuWeb.log", "w") as logfile:
    logfile.write("")
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("EmuWeb.log"), RichHandler()],
)
SYSTEMS = ["nes", "snes", "n64", "megadrive", "gamegear", "flash"]
GAMEDISPLAYNAMEREGEXES = [re.compile(r" \(.*\)"), re.compile(r" \[.*\]")]
indexcontents = """<body class="bg-dark fs-2">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
<title>EmuWeb Home</title>
<link rel="stylesheet" href="style.css">
<ul>
<li><h1 class="text-light m-2">EmuWeb</h1></li>"""

if os.path.exists("output/games"):
    shutil.rmtree("output/games")

shutil.copytree("games", "output/games")
if os.path.exists("output/artwork"):
    shutil.rmtree("output/artwork")

shutil.copytree("artwork", "output/artwork")
shutil.copy("templates/style.css", "output/style.css")


def make_player(gamefile, system, htmlname):
    with open(f"templates/{system}.html") as template:
        player_content = template.read()
    player_content = player_content.replace("$GAMEFILE", gamefile)
    with open(f"output/{htmlname}.html", "w") as output:
        output.write(player_content)


for system in SYSTEMS:
    for game in os.listdir(os.path.join("games", system)):
        gamepath = os.path.join("games", system, game)
        if game == "info.txt":
            continue

        if os.path.isfile(gamepath):
            gamedisplayname = os.path.splitext(game)[0]
            for regex in GAMEDISPLAYNAMEREGEXES:
                gamedisplayname = regex.sub("", gamedisplayname)
            gamedisplayname = gamedisplayname.replace(" - ", ";")
            gamedisplayname = gamedisplayname.replace("-", " ")
            gamedisplayname = gamedisplayname.replace(";", " - ")
            gamedisplayname = gamedisplayname.replace("_", " ")
            gamedisplayname = gamedisplayname.title()
            gamedisplayname += " "
            logging.info(f"Creating page for {game}")
            make_player(gamepath, system, game)
            logging.info(f"Checking for artwork for {game}")
            artworkpath = os.path.join("artwork", f"{game}.png")
            logging.info(f"Adding {game} to index")
            if os.path.isfile(artworkpath):
                indexcontents += f'<li><a href="{game}.html" class="text-light text-decoration-none"><img src="{artworkpath}"><br>{gamedisplayname}</a><span class="badge bg-primary">{system}</span></li>\n'
                continue
            indexcontents += f'<li><a href="{game}.html" class="text-light text-decoration-none">{gamedisplayname}</a><span class="badge bg-primary">{system}</span></li>\n'

logging.info("Creating index.html")
indexcontents += "</ul></body>"
with open("output/index.html", "w") as indexfile:
    indexfile.write(indexcontents)
