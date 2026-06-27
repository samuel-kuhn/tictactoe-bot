from selenium import webdriver
from webbot import Webbot

# Initialize Webdriver
driver = webdriver.Chrome()
driver.get("https://papergames.io/en/tic-tac-toe")

bot = Webbot(driver)

bot.setup()

# play the game
game = 1
while True:
    bot.play_game()
    print(f'Played game {str(game)}')