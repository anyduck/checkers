from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QApplication
from PySide2.QtCore import QSize, QRect, QPropertyAnimation, QParallelAnimationGroup, Qt
from client import Network
from game import Game
import sys, os


def res_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def connect():
    global n
    n = Network()
    return n


class GameMenu():
    def __init__(self, menu):
        menu.setMinimumSize(QSize(320, 200))
        menu.setMaximumSize(QSize(320, 200))
        menu.setWindowIcon(QIcon(res_path("images\\icon.ico")))
        menu.setWindowTitle("Checkers")
        menu.setStyleSheet("QMainWindow {background-color: rgb(255, 255, 255)}\n"
"QPushButton {background-color: rgb(240, 240, 240);border: 1px solid rgb(240, 240, 240);}\n"
"QPushButton:hover {background-color: rgb(249, 249, 249);border: 1px solid rgb(249, 249, 249);}\n"
"QLineEdit {border: 1px solid rgb(240, 240, 240);}")
        self.InitWindow()

    def InitWindow(self):
        self.Logo = QLabel(menu)
        self.Logo.setPixmap(QPixmap(res_path("images\\logo.png")))
        self.Logo.setGeometry(QRect(0, 0, 320, 98))

        self.StartMultiplayer = QPushButton("Start", menu)
        self.StartMultiplayer.setGeometry(QRect(360, 146, 280, 40))
        self.StartMultiplayer.clicked.connect(self.startMulti)

        self.PlayerName = QLineEdit("Player", menu)
        self.PlayerName.setMaxLength(8)
        self.PlayerName.setAlignment(Qt.AlignCenter)
        self.PlayerName.setGeometry(QRect(360, 100, 280, 40))

        self.MultiplayerMode = QPushButton("Play Multiplayer Game", menu)
        self.MultiplayerMode.setGeometry(QRect(20, 100, 280, 40))
        self.MultiplayerMode.clicked.connect(self.doMultiplayerMode)

        self.Singleplayer = QPushButton("Play with Computer", menu)
        self.Singleplayer.setGeometry(QRect(20, 146, 280, 40))

        self.Backward = QPushButton('←', menu)
        self.Backward.setGeometry(QRect(-30, 0, 30, 30))
        self.Backward.clicked.connect(self.doMenu)
        self.Backward.setStyleSheet('background-color: #FFFFFF; border: none')

        self.doEmergence()

    def doEmergence(self):
        self.animation = QParallelAnimationGroup()

        animMulti = QPropertyAnimation(self.Singleplayer, b"geometry")
        animMulti.setDuration(300)
        animMulti.setStartValue(QRect(320, 146, 280, 40))
        animMulti.setEndValue(QRect(20, 146, 280, 40))

        animSingle = QPropertyAnimation(self.MultiplayerMode, b"geometry")
        animSingle.setDuration(300)
        animSingle.setStartValue(QRect(320, 100, 280, 40))
        animSingle.setEndValue(QRect(20, 100, 280, 40))

        animLogo = QPropertyAnimation(self.Logo, b"geometry")
        animLogo.setDuration(300)
        animLogo.setStartValue(QRect(320, 0, 320, 98))
        animLogo.setEndValue(QRect(0, 0, 320, 98))

        self.animation.addAnimation(animMulti)
        self.animation.addAnimation(animSingle)
        self.animation.addAnimation(animLogo)

        self.animation.start()

    def doMultiplayerMode(self):
        self.animation = QParallelAnimationGroup()

        animStart = QPropertyAnimation(self.StartMultiplayer, b"geometry")
        animStart.setDuration(300)
        animStart.setStartValue(QRect(320, 146, 280, 40))
        animStart.setEndValue(QRect(20, 146, 280, 40))

        animName = QPropertyAnimation(self.PlayerName, b"geometry")
        animName.setDuration(300)
        animName.setStartValue(QRect(320, 100, 280, 40))
        animName.setEndValue(QRect(20, 100, 280, 40))

        animMulti = QPropertyAnimation(self.Singleplayer, b"geometry")
        animMulti.setDuration(300)
        animMulti.setStartValue(QRect(20, 146, 280, 40))
        animMulti.setEndValue(QRect(-280, 146, 280, 40))

        animSingle = QPropertyAnimation(self.MultiplayerMode, b"geometry")
        animSingle.setDuration(300)
        animSingle.setStartValue(QRect(20, 100, 280, 40))
        animSingle.setEndValue(QRect(-280, 100, 280, 40))

        animBackward = QPropertyAnimation(self.Backward, b"geometry")
        animBackward.setDuration(100)
        animBackward.setStartValue(QRect(-30, 0, 30, 30))
        animBackward.setEndValue(QRect(0, 0, 30, 30))

        self.animation.addAnimation(animStart)
        self.animation.addAnimation(animName)
        self.animation.addAnimation(animMulti)
        self.animation.addAnimation(animSingle)
        self.animation.addAnimation(animBackward)

        self.animation.start()
        self.PlayerName.selectAll()

    def doMenu(self):
        self.animation = QParallelAnimationGroup()

        animStart = QPropertyAnimation(self.StartMultiplayer, b"geometry")
        animStart.setDuration(300)
        animStart.setEndValue(QRect(320, 146, 280, 40))
        animStart.setStartValue(QRect(20, 146, 280, 40))

        animName = QPropertyAnimation(self.PlayerName, b"geometry")
        animName.setDuration(300)
        animName.setEndValue(QRect(320, 100, 280, 40))
        animName.setStartValue(QRect(20, 100, 280, 40))

        animMulti = QPropertyAnimation(self.Singleplayer, b"geometry")
        animMulti.setDuration(300)
        animMulti.setEndValue(QRect(20, 146, 280, 40))
        animMulti.setStartValue(QRect(-280, 146, 280, 40))

        animSingle = QPropertyAnimation(self.MultiplayerMode, b"geometry")
        animSingle.setDuration(300)
        animSingle.setEndValue(QRect(20, 100, 280, 40))
        animSingle.setStartValue(QRect(-280, 100, 280, 40))

        animBackward = QPropertyAnimation(self.Backward, b"geometry")
        animBackward.setDuration(100)
        animBackward.setStartValue(QRect(0, 0, 30, 30))
        animBackward.setEndValue(QRect(-30, 0, 30, 30))

        self.animation.addAnimation(animStart)
        self.animation.addAnimation(animName)
        self.animation.addAnimation(animMulti)
        self.animation.addAnimation(animSingle)
        self.animation.addAnimation(animBackward)

        self.animation.start()

    def startMulti(self):
        try:
            bo = connect()
            game = Game(self.PlayerName.text(), bo)
            menu.hide()
            game.multiplayer()
            menu.show()
        except:
            self.doMenu()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = QMainWindow()
    ui = GameMenu(menu)
    menu.show()
    sys.exit(app.exec_())
