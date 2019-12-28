C:\Python37\python.exe -OO C:\Python37\Scripts\pyinstaller.exe --noconfirm --log-level=WARN -w^
    --clean ^
    --onefile ^
    --add-data="src\images\men_white.png;images" ^
    --add-data="src\images\men_black.png;images" ^
    --add-data="src\images\king_white.png;images" ^
    --add-data="src\images\king_black.png;images" ^
    --add-data="src\images\king_black.png;images" ^
    --add-data="src\images\icon.png;images" ^
    --add-data="src\images\logo.png;images" ^
    --add-data="src\images\icon.ico;images" ^
    --add-data="src\fonts\Segoe UI Bold Italic.ttf;fonts" ^
    --add-data="src\fonts\Segoe UI Italic.ttf;fonts" ^
    --hidden-import=pygame ^
    --hidden-import=board ^
    --hidden-import=client ^
    --icon=src\images\icon.ico ^
    src\launcher.py