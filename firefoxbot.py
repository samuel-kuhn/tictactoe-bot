from selenium import webdriver
from webbot import Webbot
from selenium.webdriver.firefox.options import Options

run = 1
game = 1


def main():
    global game
    options = Options()
    options.add_argument("--headless")
    options.set_preference("media.volume_scale", "0.0")
    driver = webdriver.Firefox(options=options)

    try:
        # Initialize Webdriver
        driver.get("https://papergames.io/en/tic-tac-toe")

        bot = Webbot(driver)
        bot.setup()

        # play the game
        while True:
            bot.play_game()
            print(f'Played game {str(game)}')
            game += 1

    except Exception as exception:
        global run
        driver.save_screenshot(f'final{run}.png')
        with open(f'final{run}.log', 'w') as log:
            log.write("Played " + str(game) + " games")
            log.write(str(exception))
            log.close()
        print("closing driver")
        driver.quit()
        run += 1
        print("run " + str(run) + " failed")


if __name__ == '__main__':
    while True:
        main()
