@echo off
setlocal

echo =============================
echo Docker Build & Push Script
echo =============================

REM Ask input
set /p NAME=Enter image name:
set /p OWNER=Enter GHCR owner (username/org):

echo.
echo 🔨 Building Docker image...
docker build -t %NAME% .

if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b
)

echo.
echo 🚀 Running Docker container...
docker run %NAME%

echo.
echo ⏸️ Press any key to continue tagging & pushing...
pause >nul

echo.
echo 🏷️ Tagging image...
docker tag %NAME% ghcr.io/%OWNER%/%NAME%:latest

echo.
echo 📤 Pushing to GHCR...
docker push ghcr.io/%OWNER%/%NAME%:latest

echo.
echo ✅ Done!
pause
