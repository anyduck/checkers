C:\Python37\python.exe -OO C:\Python37\Scripts\pyinstaller.exe --noconfirm --log-level=WARN -w^
    --clean ^
    --onefile ^
    --add-data="images\men_white.png;images" ^
    --add-data="images\men_black.png;images" ^
    --add-data="images\king_white.png;images" ^
    --add-data="images\king_black.png;images" ^
    --add-data="images\king_black.png;images" ^
    --add-data="images\icon.png;images" ^
    --add-data="images\logo.png;images" ^
    --add-data="images\icon.ico;images" ^
    --add-data="fonts\Segoe UI Bold Italic.ttf;fonts" ^
    --add-data="fonts\Segoe UI Italic.ttf;fonts" ^
    --hidden-import=pygame ^
    --hidden-import=board ^
    --hidden-import=client ^
    --icon=images\icon.ico ^
    launcher.py