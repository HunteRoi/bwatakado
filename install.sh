#!/bin/bash

echo "Checking for Python 3 installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed, installing it now..."
    distro=$(lsb_release -si)
  
    if [ "$distro" == "Fedora" ]; then
        echo "Installing dependencies for Fedora..."
        sudo dnf install -y python3-pip
    elif [ "$distro" == "Ubuntu" ] || [ "$distro" == "Debian" ]; then
        echo "Installing dependencies for Debian-based distributions..."
        sudo apt-get install -y python3-pip
    elif [ "$distro" == "CentOS" ]; then
        echo "Installing dependencies for CentOS..."
        sudo yum install -y python3-pip
    else
        echo "Unsupported distribution, please install Python 3 manually."
        exit 1
    fi
  
    unset distro
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment and installing dependencies..."
    python3 -m venv venv
    sudo pip3 install -r requirements.txt
fi

echo "Starting the application"
python3 bwatakado.py
