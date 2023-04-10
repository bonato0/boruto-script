#!/bin/bash

# Atualiza pacotes apt
sudo apt update

# Instala o Python e Pip
sudo apt install -y python3
sudo apt install -y python3-pip

# Instala o Ansible
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt update
sudo apt install -y ansible

# Deleta arquivo Config na pasta .ssh
sudo rm ~/.ssh/config

# Tira proteção de hosts conhecidos
echo "Host *
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
ServerAliveInterval 120" >> ~/.ssh/config

# Instala bibliotecas necessárias
pip3 install argparse
pip3 install linode_api4
