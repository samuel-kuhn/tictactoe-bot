import time
import os
from selenium.webdriver.common.by import By
import selenium.webdriver.remote.webelement as webelement
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from board import Board
from player import Player
from invincibot import InvinciBot

load_dotenv()


def get_tags_of_element(element) -> list:
    tags = []
    elements = element.find_elements(By.CSS_SELECTOR, '*')
    for element in elements:
        tags.append(element.tag_name)
    return tags


def get_field_value(field):
    tag_list = get_tags_of_element(field)
    return None if tag_list == [] else "set"


class Webbot:
    def __init__(self, driver):
        self.driver = driver
        self.comparison_board = [[None for y in range(3)] for x in range(3)]
        self.bot = InvinciBot(Player.x)
        self.opponent = Player.o

    def clean_fields(self):
        cell = self.driver.find_element(By.CLASS_NAME, 'cell-0-0')
        hover = ActionChains(self.driver).move_to_element(cell)
        hover.perform()
        player = self.driver.find_element(By.XPATH, f'//span[text()="{os.getenv("DISPLAY_NAME")}"]')
        hover = ActionChains(self.driver).move_to_element(player)
        hover.perform()

    def get_button_by_text(self, text):
        return self.driver.find_element(By.XPATH, f'//button[text()="{text}"]')

    def get_fields(self):
        field_elements = self.driver.find_elements(By.CLASS_NAME, 'grid-item')
        field_value_list = []
        for field_element in field_elements:
            field_value_list.append(get_field_value(field_element))
        fields = [field_value_list[i:i + 3] for i in range(0, len(field_value_list), 3)]
        return fields

    def get_last_move(self):
        current_gameboard = self.get_fields()
        for row in range(3):
            for col in range(3):
                if current_gameboard[row][col] != self.comparison_board[row][col]:
                    return row, col

    def wait_for_game(self) -> bool:
        """
        Waits until a game is found. Looks for the 'Abort game' button on the screen.
        :return: True if the button was found, False if not after 1 minute.
        """
        timeout = 120
        while timeout > 0:
            time.sleep(0.5)
            print('waiting for game')
            timeout -= 1
            try:
                self.get_button_by_text(' Abort game ')
                return True
                break
            except Exception:
                pass
        return False

    def start_game(self):
        """
        Starts a game and exits if a game was found.
        """
        print('starting game')
        button = self.get_button_by_text(' Play online ')
        button.click()
        time.sleep(1)
        if not self.wait_for_game():
            exit_button = self.driver.find_element(By.CLASS_NAME, 'leave-room')
            exit_button.click()
            time.sleep(1)
            print('No game found. retrying')
            self.start_game()
        print('game started')

    def wait_for_leave_button(self) -> webelement:
        while True:
            time.sleep(0.5)
            print('waiting for game to finish')
            try:
                button = self.get_button_by_text('Leave room')
                break
            except Exception:
                pass
        return button

    def circle_on_player(self):
        player = self.driver.find_element(By.XPATH, f'//span[text()="{os.getenv("DISPLAY_NAME")}"]')
        player_div = player.find_element(By.XPATH, '../../app-user-avatar/div')
        return True if 'svg' in get_tags_of_element(player_div) else False

    def board_is_present(self) -> bool:
        board_tag = self.driver.find_elements(By.TAG_NAME, 'app-tic-tac-toe')
        return True if board_tag != [] else False

    def play_move(self, row, col):
        print('play move: ' + str([row, col]))
        field = self.driver.find_element(By.CLASS_NAME, f'cell-{row}-{col}')
        field.click()

    def bot_play(self, b):
        move = self.bot.select_move(b)
        self.play_move(move[0], move[1])
        b.make_move(move[0], move[1], Player.x)
        self.update_comparison_board(move[0], move[1])
        time.sleep(2)

    def first_play(self, b):
        self.play_move(0, 0)
        b.make_move(0, 0, Player.x)
        self.update_comparison_board(0, 0)
        time.sleep(2)

    def update_comparison_board(self, row: int, col: int):
        self.comparison_board = self.get_fields()
        self.comparison_board[row][col] = "set"

    def setup(self):
        time.sleep(3)

        # consent
        print('giving consent')
        button = self.driver.find_element(By.CLASS_NAME, 'fc-cta-consent')
        button.click()
        time.sleep(1)

        # login
        print('logging in')
        button = self.get_button_by_text('Login')
        button.click()
        time.sleep(1)
        email = self.driver.find_element(By.XPATH, '//input[@type="email"]')
        email.send_keys(os.getenv("EMAIL"))
        password = self.driver.find_element(By.XPATH, '//input[@type="password"]')
        password.send_keys(os.getenv("PASSWORD"))
        button = self.get_button_by_text(' Login ')
        button.click()
        time.sleep(2)

    def play_game(self):
        b = Board()
        self.comparison_board = [[None for y in range(3)] for x in range(3)]

        # start game
        self.start_game()
        time.sleep(1)
        self.clean_fields()
        time.sleep(1)

        # play
        while True:
            if self.board_is_present() and not self.circle_on_player():
                time.sleep(0.5)
                print('waiting for turn')

            elif self.board_is_present() and self.circle_on_player():
                opponent_move = self.get_last_move()
                print('opponent move: ' + str(opponent_move))
                if opponent_move is None:
                    self.first_play(b)
                else:
                    b.make_move(opponent_move[0], opponent_move[1], self.opponent)
                    self.bot_play(b)
            else:
                break

        # leave room
        leave_button = self.wait_for_leave_button()
        time.sleep(1)
        print('leaving room')
        leave_button.click()
        time.sleep(1)
