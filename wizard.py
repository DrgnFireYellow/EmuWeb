import json
import os
import shutil
import sys
from subprocess import run

import questionary
import requests
from rich import print
from yaml import Dumper, Loader, dump, load

SYSTEMS = ["nes", "snes", "n64", "nds", "megadrive", "gamegear", "flash", "scratch"]
with open("config.yml") as configfile:
    config = load(configfile.read(), Loader=Loader)


def projectidvalidator(projectid):
    try:
        int(projectid)
    except ValueError:
        return False
    return True


while True:
    print("[bold] Welcome to the EmuWeb management wizard![/]")
    action = questionary.select(
        "What would you like to do?",
        [
            "Copy a game file",
            "Add a Scratch Game",
            "Remove a Game",
            "Enable/Disable Systems",
            "Regenerate Output",
            "Quit",
        ],
    ).ask()

    if action == "Copy a game file":
        gamespath = os.path.join(os.getcwd(), "games")
        os.chdir(os.path.expanduser("~"))
        file = questionary.path("Please select a file to copy:").ask()
        if file == None:
            continue
        system = questionary.select(
            "Please select the system that the game is for:", SYSTEMS
        ).ask()
        if system == None:
            continue
        print("[bold lime]Copying file...[/]")
        shutil.copy(file, os.path.join(gamespath, system))

    elif action == "Add a Scratch Game":
        projectid = questionary.text(
            "Please enter the scratch project id:", validate=projectidvalidator
        ).ask()
        if projectid == None:
            continue
        print("Fetching project name...")
        projectdata = json.loads(
            requests.get(
                "https://api.scratch.mit.edu/projects/" + projectid, timeout=60
            ).content
        )
        projecttitle = projectdata["title"].replace("/", "|")
        print("Adding project " + projecttitle + "...")
        with open(
            os.path.join("games", "scratch", f"{projecttitle}.txt"), "w"
        ) as projectfile:
            projectfile.write(projectid)
        print("Project added, regenerate output to see your changes")
    elif action == "Remove a Game":
        os.chdir("games")
        gamepath = questionary.path(
            "Please enter the path of the game to remove (press tab):"
        ).ask()
        if gamepath == None:
            continue
        if "info.txt" not in gamepath:
            if os.path.isdir(gamepath):
                print("[bold red]Please do not select a directory.[/]")
            else:
                artworkpath = os.path.join(
                    "artwork", f"{os.path.basename(gamepath)}.png"
                )
                print(artworkpath)
                if questionary.confirm(
                    f"Are you sure you want to remove {gamepath}?", False
                ).ask():
                    os.remove(gamepath)
                    if os.path.isfile(artworkpath):
                        os.remove(artworkpath)
                    print("Game removed, regenerate output to see your changes")
                else:
                    print("[bold red]Cancelling...[/]")
        else:
            print("[bold red]info.txt is not a game[/]")
    elif action == "Enable/Disable Systems":
        enabledsystems = questionary.checkbox(
            "Please select the systems to enable:", SYSTEMS
        ).ask()
        config["enabled-systems"] = enabledsystems
        with open("config.yml", "w") as configfile:
            dump(config, configfile, Dumper=Dumper)
    elif action == "Regenerate Output":
        run([sys.executable, "main.py"])
    elif action == "Quit":
        quit()
