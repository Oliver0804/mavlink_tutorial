@echo off
echo conda activate mavlink
:: 初始化Conda環境
call %UserProfile%\Anaconda3\Scripts\activate.bat

:: 激活指定的Conda環境
call conda activate mavlink
echo Starting MAVProxy on COM...
start cmd /k mavproxy.exe --master=COM14 --out=127.0.0.1:14550 --out=127.0.0.1:14560 --map

echo Starting MAVProxy on COM...
start cmd /k mavproxy.exe --master=COM15 --out=127.0.0.1:14551 --out=127.0.0.1:14561 --map

echo Running Python script...
python followRTL.py

echo Script execution finished.
pause
