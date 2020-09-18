| :warning: WARNING for multiplayer |
| :-------------------------------- |
| The pickle module, that used in this project, is not secure.<br />It is possible to construct malicious pickle data which will execute arbitrary code during unpickling.<br />Safer serialization formats such as json must be used. |
# Сheckers v1.0
Now you can play the classic childhood game. A game against the computer is under development
The game is written in python with the ability to multiplayer
  - Server included in server.py and required board.py and piece.py
  - Don't forget to start server before starting multiplayer in your local network
  - Client side included in game.py and required board.py and client.py
 ## Requirements
  - Required PyGame for console version
  - Required PyGame, PySide2 for version with launcher
 ## Building
Have ability to compile in executable file by PyInstaller from build.bat in each variation
  - PyInstaller required Python 3.7. Change path to your folder with Python 3.7 in *.bat
