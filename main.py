import os
import shutil

SYSTEMS = ["nes", "snes", "n64", "megadrive"]
indexcontents = "<link rel=\"stylesheet\" href=\"style.css\">\n<ul>\n"

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
            print(f"Creating page for {game}")
            make_player(gamepath, system, game)
            print(f"Checking for artwork for {game}")
            artworkpath = os.path.join("artwork", f"{game}.png")
            print(f"Adding {game} to index")
            if os.path.isfile(artworkpath):
                indexcontents += f"<li><a href=\"{game}.html\"><img src=\"{artworkpath}\"><br>{game}</a></li>\n"
                continue
            indexcontents += f"<li><a href=\"{game}.html\">{game}</a></li>\n"

print("Creating index.html")
indexcontents += "</ul>"
with open("output/index.html", "w") as indexfile:
    indexfile.write(indexcontents)