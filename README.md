# EmuWeb
[![Documentation](https://img.shields.io/badge/Documentation-blue?style=for-the-badge)](https://drgnfireyellow.github.io/EmuWeb)

The Open Source Retro Emulation Frontend for the Web

NOTE: At this time I am unable to create templates for platforms other than megadrive, gamegear, n64, nes, and snes. If you would like to help add more templates, feel free to create a pull request.

## Requirements

- Python 3.12

## Setup

### Setup with Docker

1. Create the container with `docker run --name EmuWeb -p 8080:80 -v ~/EmuWeb/games:/EmuWeb/games -v ~/EmuWeb/artwork:/EmuWeb/artwork ghcr.io/drgnfireyellow/emuweb:stable`. This will create the container, make the page available on port 8080, map the games folder to ~/EmuWeb/games, and map the artwork folder to ~/EmuWeb/artwork.
2. Add your legally obtained roms to the games folder in the sub-folder for the appropriate system.
3. (Optional) Add game artwork (such as box art) to the artwork folder in png format named as [rom name].png. For example, if I had a rom called SuperMario64.z64 I would name my artwork file SuperMario64.z64.png.
4. Restart the container.
5. Open your web browser and connect to the forwarded port.

### Standalone Setup

1. Clone the repository from GitHub or download and extract the zip.
2. Add your legally obtained roms to the games folder in the sub-folder for the appropriate system.
3. (Optional) Add game artwork (such as box art) to the artwork folder in png format named as [rom name].png. For example, if I had a rom called SuperMario64.z64 I would name my artwork file SuperMario64.z64.png.
4. Run main.py.
5. Start any web server in the output folder.
6. Open your web browser and connect to the web server.

## Credits

The template files are modified versions of files from the emulatorjs.org code editor.
