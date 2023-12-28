import logging
import os
import re
import shutil
from string import punctuation

import questionary
import requests
from bs4 import BeautifulSoup
from rich import print
from rich.align import Align
from rich.logging import RichHandler
from rich.table import Table

with open("EmuWeb.log", "w") as logfile:
    logfile.write("")
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("EmuWeb.log"), RichHandler()],
)
SYSTEMS = ["nes", "snes", "n64", "megadrive", "gamegear", "flash"]
GAMEDISPLAYNAMEREGEXES = [re.compile(r" \(.*\)"), re.compile(r" \[.*\]")]
ARTWORKURLS = {
    "nes": "http://thumbnails.libretro.com/Nintendo%20-%20Nintendo%20Entertainment%20System/Named_Boxarts/",
    "snes": "http://thumbnails.libretro.com/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/Named_Boxarts/",
    "n64": "http://thumbnails.libretro.com/Nintendo%20-%20Nintendo%2064/Named_Boxarts/",
    "megadrive": "http://thumbnails.libretro.com/Sega%20-%20Mega%20Drive%20-%20Genesis/Named_Boxarts/",
    "gamegear": "http://thumbnails.libretro.com/Sega%20-%20Game%20Gear/Named_Boxarts/",
}
artworksoups = {}
indexcontents = """<body class="bg-dark fs-2">
<link rel="icon" href="/favicon.png">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css">
<script src="//cdnjs.cloudflare.com/ajax/libs/list.js/2.3.1/list.min.js"></script>
<title>EmuWeb Home</title>
<link rel="stylesheet" href="style.css">
<h1 class="text-light m-2">EmuWeb</h1>
<div id="gamelist">
<i class="bi bi-search text-light ms-1"></i><input class="search ms-2 mb-2 rounded-pill border-dark" type="search" placeholder="Search...">
<ul class="list">"""
downloadartwork = questionary.confirm(
    "Would you like to attempt to automatically download artwork?"
).ask()
if downloadartwork:
    for system in SYSTEMS:
        if system in ARTWORKURLS:
            try:
                artworksoups[system] = BeautifulSoup(
                    requests.get(ARTWORKURLS[system], timeout=60).content, "html.parser"
                )
            except requests.Timeout:
                logging.critical(
                    "Unable to download artwork manifests, disabling artwork downloader."
                )
                downloadartwork = False
gamelisttable = Table(title="Games Found")
gamelisttable.add_column("Game")
gamelisttable.add_column("File")
gamelisttable.add_column("System")
if os.path.exists("output/games"):
    shutil.rmtree("output/games")

shutil.copytree("games", "output/games")
if os.path.exists("output/artwork"):
    shutil.rmtree("output/artwork")

shutil.copy("templates/style.css", "output/style.css")
shutil.copy("templates/favicon.png", "output/favicon.png")


def make_player(gamefile, system, htmlname):
    with open(f"templates/{system}.html") as template:
        player_content = template.read()
    player_content = player_content.replace("$GAMEFILE", gamefile)
    with open(f"output/{htmlname}.html", "w") as output:
        output.write(player_content)


for system in SYSTEMS:
    indexcontents += (
        f'<a href="#{system}" class="btn btn-secondary me-2 mb-2">{system.upper()} </a>'
    )

for system in SYSTEMS:
    indexcontents += f'<h2 class="text-light text-decoration-underline" id="{system}">{system.upper()}</h2>'
    for game in os.listdir(os.path.join("games", system)):
        gamepath = os.path.join("games", system, game)
        if game == "info.txt":
            continue

        if os.path.isfile(gamepath):
            gamedisplayname = os.path.splitext(game)[0]
            for regex in GAMEDISPLAYNAMEREGEXES:
                gamedisplayname = regex.sub("", gamedisplayname)
            gamedisplayname = gamedisplayname.replace(" - ", " ")
            gamedisplayname = gamedisplayname.replace("-", " ")
            gamedisplayname = gamedisplayname.replace("_", " ")
            for symbol in punctuation:
                gamedisplayname = gamedisplayname.replace(symbol, "")
            gamedisplayname = gamedisplayname.title()
            gamedisplayname += " "
            logging.info(f"Creating page for {game}")
            make_player(gamepath, system, game)
            logging.info(f"Checking for artwork for {game}")
            artworkpath = os.path.join("artwork", f"{game}.png")
            if downloadartwork:
                if system in artworksoups:
                    if not os.path.exists(artworkpath):
                        try:
                            logging.info(f"Downloading artwork for {game}")
                            artworkurl = (
                                artworksoups[system]
                                .find(string=re.compile(rf"{gamedisplayname}"))
                                .parent["href"]
                            )
                            with open(f"artwork/{game}.png", "wb") as artworkfile:
                                artworkfile.write(
                                    requests.get(
                                        ARTWORKURLS[system] + artworkurl, timeout=60
                                    ).content
                                )
                        except (TypeError, AttributeError, requests.Timeout):
                            logging.error(f"Unable to download artwork for {game}")
            logging.info(f"Adding {game} to index")
            gamelisttable.add_row(gamedisplayname, game, system)
            if os.path.isfile(artworkpath):
                indexcontents += f'<li><a href="{game}.html" class="text-light text-decoration-none name"><img src="{artworkpath}"><br>{gamedisplayname}</a><span class="badge bg-primary">{system}</span></li>\n'
                continue
            indexcontents += f'<li><a href="{game}.html" class="text-light text-decoration-none name">{gamedisplayname}</a><span class="badge bg-primary">{system}</span></li>\n'

shutil.copytree("artwork", "output/artwork")
logging.info("Creating index.html")
indexcontents += '</ul></div><script>var gameList = new List("gamelist", {valueNames: ["name"]});</script></body>'
with open("output/index.html", "w") as indexfile:
    indexfile.write(indexcontents)
print(Align.center(gamelisttable))
