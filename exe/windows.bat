@RD /S /Q build
@RD /S /Q dist
call activate cldvis
pyinstaller cldvis.spec