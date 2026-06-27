# tictactoe-bot

A bot to get to the top of the leaderboard on [papergames.io](https://papergames.io/en/tic-tac-toe).

Please use responsibly :)


Copied machine learning functions for TicTacToe from [here](https://github.com/morgankenyon/RandomML).

## Requirements:

- python installed
- pip installed
- chorme or firefox installed with the according driver

[Firefoxdriver in Linux](https://dev.to/eugenedorfling/installing-the-firefox-web-driver-on-linux-for-selenium-d45)

[Chomedriver](https://developer.chrome.com/docs/chromedriver/get-started?hl=de)


## Auto Setup

For a easy setup you need to complete 2 simple steps:

- Go to [papergames.io](https://papergames.io/en/tic-tac-toe) and create a user account
- run either the ```firefoxbot.sh``` or ```chromebot.sh``` depending on what is installed

During the setup you will be asked for credentials to use.

## Manual Setup

### Set environment variables 

Email and password are imported as environment variables.

To run the chromebot you need to set email and password as environment variables or save them in a .env file:

```
EMAIL=my.email@example.net
PASSWORD=mysecurepassword
DISPLAY_NAME='your ingame username'
```

### Install the python requirements

(Doing this in a virtual environment is recommended)

To install the packages simply run:

```
pip install -r requirements.txt
```






## Errors:

### Profile Missing

Your Firefox profile cannot be loaded. It may be missing or inaccessible.

#### Solution:

[Fix Firefox Profile Error](https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04#:~:text=Uninstall%20the%20Firefox%20Snap)
