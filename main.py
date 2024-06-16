import game
import bots
import gui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys

def main():
    app = QApplication(sys.argv)

    # Instantiate some SpaceBots (use your own SpaceBot class here)
    bot1 = bots.RandomAttacker("Randomizied")
    bot2 = bots.AttackTheWeakest("AttackTheWeakest")
    bot3 = bots.SuperSmart("Smart")
    bot_list = [bot1, bot2, bot3]

    new_game = game.BattleGame(bot_list)
    new_game.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

