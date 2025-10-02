@echo off
chcp 65001 >nul
echo =====================================
echo     图片收纳器自动Release发布脚本
echo =====================================

REM 检查是否安装了GitHub CLI
gh --version >nul 2>&1
if errorlevel 1 (
    echo GitHub CLI 未安装！
    echo 请访问 https://cli.github.com/ 下载安装
    echo 或使用手动方式发布Release
    pause
    exit /b 1
)

set /p VERSION="请输入版本号 (例如: v1.0.0): "
if "%VERSION%"=="" (
    echo 版本号不能为空！
    pause
    exit /b 1
)

echo.
echo 正在检查可执行文件...
if not exist "dist\图片收纳器.exe" (
    echo 可执行文件不存在！请先运行 build.bat 进行打包
    pause
    exit /b 1
)

echo 正在创建并推送Git标签...
git tag -a %VERSION% -m "图片收纳器 %VERSION% 发布"
git push origin %VERSION%

echo.
echo 正在创建GitHub Release...
gh release create %VERSION% "dist\图片收纳器.exe" ^
    --title "图片收纳器 %VERSION% - 稳定版本" ^
    --notes "## 🎉 图片收纳器 %VERSION% 发布！

### ✨ 主要功能
- 支持图片格式：.psb .psd .tif .jpg .jpeg .png .bmp .webp .gif
- 支持视频格式：.mp4 .mov .wmv .3gp .avi .flv  
- 根据文件修改时间按年月自动分类
- 递归搜索子目录
- 智能文件重名处理
- GUI界面，窗体居中显示

### 📦 使用说明
1. 下载 **图片收纳器.exe** 文件
2. 双击运行即可使用
3. 无需安装Python环境

### 🔧 系统要求
- Windows 7/8/10/11
- 64位操作系统

### 💝 致谢
© 2025 速光网络软件开发  
抖音号关注：dubaishun12"

if errorlevel 0 (
    echo =====================================
    echo ✅ Release发布成功！
    echo 访问地址：https://github.com/您的用户名/图片收纳器/releases
    echo =====================================
) else (
    echo ❌ Release发布失败，请检查权限或网络连接
)

pause