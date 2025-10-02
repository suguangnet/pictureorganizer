@echo off
chcp 65001 >nul
echo =====================================
echo      图片收纳器 Release 发布脚本
echo =====================================

set /p VERSION="请输入版本号 (例如: v1.0.0): "
if "%VERSION%"=="" (
    echo 版本号不能为空！
    pause
    exit /b 1
)

echo.
echo 正在创建Git标签...
git tag -a %VERSION% -m "图片收纳器 %VERSION% 发布"

echo 推送标签到GitHub...
git push origin %VERSION%

echo.
echo =====================================
echo Git标签已创建并推送到GitHub！
echo.
echo 接下来请手动完成以下步骤：
echo 1. 访问: https://github.com/您的用户名/图片收纳器/releases
echo 2. 点击刚创建的 "%VERSION%" 标签
echo 3. 点击 "Create release from tag"
echo 4. 填写Release标题和描述
echo 5. 上传 dist\图片收纳器.exe 文件
echo 6. 点击 "Publish release"
echo =====================================

start https://github.com
pause