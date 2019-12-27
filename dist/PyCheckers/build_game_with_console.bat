C:\Python37\python.exe -OO C:\Python37\Scripts\pyinstaller.exe --noconfirm --log-level=WARN ^
    --clean ^
    --onefile ^
    --add-data="images\men_white.png;images" ^
    --add-data="images\men_black.png;images" ^
    --add-data="images\king_white.png;images" ^
    --add-data="images\king_black.png;images" ^
    --add-data="images\icon.png;images" ^
    --add-data="fonts\Segoe UI Bold Italic.ttf;fonts" ^
    --add-data="fonts\Segoe UI Italic.ttf;fonts" ^
    --hidden-import=pygame ^
    --hidden-import=board ^
    --icon=images\icon.ico ^
    game.py