import json
import os
import shutil

import requests
from dotenv import load_dotenv
from flask import *
from steamgrid import SteamGridDB
from werkzeug.utils import secure_filename

CONSOLES = ["NES", "SNES", "N64", "GBA", "DS", "Flash"]

PLAYERS = {
    "NES": {"template": "ejs.html", "core": "nes"},
    "SNES": {"template": "ejs.html", "core": "snes"},
    "N64": {"template": "ejs.html", "core": "n64"},
    "GBA": {"template": "ejs.html", "core": "gba"},
    "DS": {"template": "ejs.html", "core": "nds"},
    "Flash": {"template": "ruffle.html", "core": None},
}

for console in CONSOLES:
    os.makedirs(os.path.join("games", console), exist_ok=True)
    os.makedirs(os.path.join("artwork", console), exist_ok=True)

if not os.path.exists("metadata.json"):
    metadata = {}

else:
    with open("metadata.json") as metadatafile:
        metadata = json.load(metadatafile)

load_dotenv()

if os.getenv("STEAMGRIDDB_API_KEY") != None:
    scraper = SteamGridDB(os.getenv("STEAMGRIDDB_API_KEY"))

app = Flask(__name__)


@app.route("/")
def index():
    games = {}

    for console in CONSOLES:
        games[console] = sorted(os.listdir(os.path.join("games", console)))

    return render_template(
        "index.html", consoles=CONSOLES, games=games, metadata=metadata
    )


@app.route("/upload/<console>", methods=["GET", "POST"])
def upload(console):
    if console not in CONSOLES:
        return "Invalid Console", 400
    else:
        if request.method == "GET":
            return render_template("upload.html")
        elif request.method == "POST":
            file = request.files["file"]
            if file.filename == "":
                return redirect(request.url)
            file.save(os.path.join("games", console, secure_filename(file.filename)))
            return redirect(f"/#console-{console}")


@app.route("/play/<console>/<game>")
def play(console, game):
    player = PLAYERS[console]
    return render_template(
        "players/" + player["template"],
        console=console,
        game=game,
        core=player["core"],
    )


@app.route("/cdn/games/<path:game>")
def games_cdn(game):
    return send_from_directory("games", game)


@app.route("/cdn/artwork/<path:game>")
def artwork_cdn(game):
    return send_from_directory("artwork", game)


@app.route("/api/scrape/<console>")
def scrape(console):
    global metadata

    for game in os.listdir(os.path.join("games", console)):
        search = scraper.search_game(os.path.splitext(game)[0])
        if len(search) > 0:
            metadata[game] = {}
            metadata[game]["name"] = search[0].name
            boxart = scraper.get_grids_by_gameid([search[0].id])[0]
            image_response = requests.get(boxart.url, stream=True)
            image_name = game + os.path.splitext(boxart.url)[-1]
            metadata[game]["image"] = image_name
            with open(os.path.join("artwork", console, image_name), "wb") as boxartfile:
                shutil.copyfileobj(image_response.raw, boxartfile)
    with open("metadata.json", "w") as metadatafile:
        json.dump(metadata, metadatafile)
    return redirect(f"/#console-{console}")


@app.route("/api/delete_game/<console>/<game>")
def delete_game(console, game):
    os.remove(os.path.join("games", console, game))

    return redirect(f"/#console-{console}")


app.run()
