#!/bin/bash
add-apt-repository ppa:deadsnakes/ppa
apt-get update 
apt-get install --no-install-recommends --no-install-suggests -y apt-utils curl git cmake build-essential
apt-get install --no-install-recommends --no-install-suggests -y python3
apt-get install --no-install-recommends --no-install-suggests -y python3-pip python3-dev python3-venv
apt-get install -y python3-requests
apt install -y python3-virtualenv
apt install pipx -y
pipx install bittensor bittensor-cli
pipx ensurepath

python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt