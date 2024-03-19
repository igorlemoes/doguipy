#!/bin/bash

#####################################################################################
## UTILIZE ESTE INSTALADOR APENAS NO SEU SERVIDOR OU VPS(TESTADO EM SERVER UBUNTU) ##
## PARA UTILIZAÇÃO EM WSL, WINDOWS OU MAC CRIE A VENV PYTHON E RODE O INSTALL.PY   ##
#####################################################################################

cat << "EOF"


$$$$$$$\             $$$$$$\            $$\ $$$$$$$\            
$$  __$$\           $$  __$$\           \__|$$  __$$\           
$$ |  $$ | $$$$$$\  $$ /  \__|$$\   $$\ $$\ $$ |  $$ |$$\   $$\ 
$$ |  $$ |$$  __$$\ $$ |$$$$\ $$ |  $$ |$$ |$$$$$$$  |$$ |  $$ |
$$ |  $$ |$$ /  $$ |$$ |\_$$ |$$ |  $$ |$$ |$$  ____/ $$ |  $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |      $$ |  $$ |
$$$$$$$  |\$$$$$$  |\$$$$$$  |\$$$$$$  |$$ |$$ |      \$$$$$$$ |
\_______/  \______/  \______/  \______/ \__|\__|       \____$$ |
 ___                         /\/                      $$\   $$ |
  |   _   _  ._ |   _  ._ _   _   _   _               \$$$$$$  |
 _|_ (_| (_) |  |_ (/_ | | | (_) (/_ _>                \______/
      _|

EOF

apt update
apt upgrade
apt install curl pip

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

pip install -r requirements.txt

clear

echo "Informe o domínio que você vai utilizar no sistema: "
read dominio

echo "Agora informe um e-mail válido: "
read email

echo "DOMAIN_BASE=$dominio" > .env
echo "EMAIL_SSL=$email" >> .env

python3 up_traefik.py
python3 up_doguipy.py
