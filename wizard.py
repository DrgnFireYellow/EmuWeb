import json
import os
import shutil
import sys
from subprocess import run

import questionary
import requests
from rich import print

SYSTEMS = ["nes", "snes", "n64", "megadrive", "gamegear", "flash", "scratch"]


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
            "Regenerate Output",
            "Quit",
        ],
    ).ask()

    if action == "Copy a game file":
        gamespath = os.path.join(os.getcwd(), "games")
        os.chdir(os.path.expanduser("~"))
        file = questionary.path("Please select a file to copy:").ask()
        system = questionary.select(
            "Please select the system that the game is for:", SYSTEMS
        ).ask()
        print("[bold lime]Copying file...[/]")
        shutil.copy(file, os.path.join(gamespath, system))

    elif action == "Add a Scratch Game":
        projectid = questionary.text(
            "Please enter the scratch project id:", validate=projectidvalidator
        ).ask()
        print("Fetching project name...")
        projectdata = json.loads(
            requests.get(
                "https://api.scratch.mit.edu/projects/" + projectid, timeout=60
            ).content
        )
        projecttitle = projectdata["title"]
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
    elif action == "Regenerate Output":
        run([sys.executable, "main.py"])
    elif action == "Quit":
        quit()
