@echo off
echo ========================================
echo   GitHub Upload Script
echo   Brukd RPA/AI Demo
echo ========================================
echo.

echo This script will help you upload to GitHub
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git is installed. Good!
echo.

REM Get GitHub username
set /p USERNAME="Enter your GitHub username: "
echo.

REM Get repository name
set /p REPONAME="Enter repository name (default: career-college-rpa-demo): "
if "%REPONAME%"=="" set REPONAME=career-college-rpa-demo
echo.

echo ========================================
echo   Step 1: Initializing Git
echo ========================================
git init
if %errorlevel% neq 0 goto :error
echo SUCCESS!
echo.

echo ========================================
echo   Step 2: Adding all files
echo ========================================
git add .
if %errorlevel% neq 0 goto :error
echo SUCCESS!
echo.

echo ========================================
echo   Step 3: Creating first commit
echo ========================================
git commit -m "Initial commit: Complete RPA/AI automation demo"
if %errorlevel% neq 0 goto :error
echo SUCCESS!
echo.

echo ========================================
echo   Step 4: Setting main branch
echo ========================================
git branch -M main
if %errorlevel% neq 0 goto :error
echo SUCCESS!
echo.

echo ========================================
echo   Step 5: Adding remote repository
echo ========================================
git remote add origin https://github.com/%USERNAME%/%REPONAME%.git
if %errorlevel% neq 0 goto :error
echo SUCCESS!
echo.

echo ========================================
echo   Step 6: Pushing to GitHub
echo ========================================
echo.
echo You may be asked for your GitHub credentials...
echo.
git push -u origin main
if %errorlevel% neq 0 goto :error
echo.
echo SUCCESS!
echo.

echo ========================================
echo   UPLOAD COMPLETE!
echo ========================================
echo.
echo Your project is now on GitHub at:
echo https://github.com/%USERNAME%/%REPONAME%
echo.
echo NEXT STEPS:
echo 1. Go to your repository on GitHub
echo 2. Enable GitHub Pages (Settings - Pages - main branch)
echo 3. Wait 2-3 minutes for deployment
echo 4. Your live demos will be at:
echo    https://%USERNAME%.github.io/%REPONAME%/
echo.
echo See GITHUB_SETUP.md for detailed instructions!
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo   ERROR OCCURRED!
echo ========================================
echo.
echo Make sure you have:
echo 1. Created the repository on GitHub first
echo    (https://github.com/new)
echo 2. Used the correct username
echo 3. Have internet connection
echo 4. Have Git configured with your credentials
echo.
echo See GITHUB_SETUP.md for help!
echo.
pause
exit /b 1

