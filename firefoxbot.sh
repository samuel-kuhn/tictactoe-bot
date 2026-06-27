#!/usr/bin/env bash

# setup
if [ ! -f ".firefox" ]; then
  if ! command -v python3 >/dev/null  2>&1
  then
    echo -e "Please make sure python3 is installed!\nExiting!"
    exit
  fi

  if ! command -v pip >/dev/null  2>&1
  then
    echo -e "Please make sure pip is installed!\nExiting!"
    exit
  fi

  if ! command -v virtualenv >/dev/null  2>&1
  then
    echo -e "installing virtualenv...\n"
    apt update >/dev/null && apt install python3-virtualenv -y >/dev/null  2>&1
  fi

  virtualenv env >/dev/null
  source env/bin/activate

  echo -e "installing all requirements...\n"
  pip install -r requirements.txt > /dev/null

  # Prompt for user input
  read -rp "Enter your email: " email
  read -rp "Enter your username: " username
  read -rsp "Enter your password: " password

  # Store input in .env file
  echo "EMAIL=$email" > .env
  echo "DISPLAY_NAME=$username" >> .env
  echo "PASSWORD=$password" >> .env

  touch .firefox
fi

# running the script
source env/bin/activate

echo -e "starting script...\n"
python3 firefoxbot.py
