install_ubuntu_amd64:
    # Install git and curl
    sudo apt-get install git curl
    # Download git repo
    git clone https://github.com/DrgnFireYellow/EmuWeb.git
    # Download and install Caddy
    curl -o caddy.deb https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_amd64.deb
    sudo apt-get install ./caddy.deb

install_ubuntu_arm64:
    # Install git and curl
    sudo apt-get install git curl
    # Download git repo
    git clone https://github.com/DrgnFireYellow/EmuWeb.git
    # Download and install Caddy
    curl -o caddy.deb https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_arm64.deb
    sudo apt-get install ./caddy.deb
