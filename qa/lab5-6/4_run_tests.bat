@echo off
cls
echo ============================================
echo   STEP 4: Running Tests on Grid
echo ============================================
echo.
echo Make sure you have started:
echo   1. Hub (1_start_hub.bat) at localhost:4444
echo   2. Chrome Node (2_start_chrome_node.bat)
echo   3. Firefox Node (3_start_firefox_node.bat)
echo.
echo Verifying Grid is ready...
echo.

REM Check if Grid is accessible
curl -s http://localhost:4444/status >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Cannot connect to Grid!
    echo.
    echo Please make sure:
    echo   1. Hub is running: http://localhost:4444/ui
    echo   2. At least one node is connected
    echo.
    pause
    exit /b 1
)

echo Grid is accessible!
echo.
echo Check Grid Console: http://localhost:4444/ui
echo Should show 2 nodes (Chrome and Firefox)
echo.
echo Starting tests...
echo ============================================
echo.

cd /d "%~dp0"
python -m pytest tests/test_ui_grid.py -v --tb=short

echo.
echo ============================================
echo   Tests Complete!
echo ============================================
pause