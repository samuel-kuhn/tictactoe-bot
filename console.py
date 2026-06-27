from board import Board
from player import Player
from invincibot import InvinciBot

b = Board()
bot = InvinciBot(Player.x)

players = {
    Player.x.value: 'Bot',
    Player.o.value: 'Player'
}


def show_winner():
    print('\n' + '_' * 30)
    b.print()

    winner = b.has_winner()
    if winner is None:
        print('\nIts a Tie!')
    else:
        winner_int = winner.value
        print('\n' + players[winner_int] + ' wins!')
    exit()


def player_move():
    b.print_numbered()
    row = int(input("Row: "))
    column = int(input("Column: "))
    b.make_move(row, column, Player.o)


def bot_move():
    move = bot.select_move(b)
    b.make_move(move[0], move[1], Player.x)


bot_move()
while True:
    show_winner() if len(b.moves) == 9 or b.has_winner() is not None else player_move()
    show_winner() if len(b.moves) == 9 or b.has_winner() is not None else bot_move()
