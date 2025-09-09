@echo off
chcp 65001 >nul
echo 正在打包图片收纳器...
echo =====================================

REM 检查是否安装了PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 正在安装PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo 安装PyInstaller失败，请检查Python环境
        pause
        exit /b 1
    )
)

REM 清理之前的构建文件
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "图片收纳器.spec" del "图片收纳器.spec"

echo 开始打包...
pyinstaller --onefile --noconsole --name "图片收纳器" image_video_organizer.py

if errorlevel 0 (
    echo =====================================
    echo 打包成功！
    echo 可执行文件位置：dist\图片收纳器.exe
    echo 文件大小：
    dir dist\*.exe
    echo =====================================
    echo 正在测试程序...
    start dist\图片收纳器.exe
) else (
    echo 打包失败，请检查错误信息
)

pause