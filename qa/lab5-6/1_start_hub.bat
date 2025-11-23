@echo off
cls
echo ============================================
echo   STEP 1: Starting Selenium Grid Hub
echo ============================================
echo.

REM Find selenium jar
for %%f in (selenium-server*.jar) do set JAR=%%f

if not defined JAR (
    echo ERROR: selenium-server jar not found!
    pause
    exit /b 1
)

echo Hub will be at: http://localhost:4444
echo Console: http://localhost:4444/ui
echo.
echo After Hub starts, run the node scripts:
echo   - 2_start_chrome_node.bat
echo   - 3_start_firefox_node.bat
echo.
echo Press Ctrl+C to stop Hub
echo ============================================
echo.

java -jar %JAR% hub --host localhost --publish-events tcp://localhost:4442 --subscribe-events tcp://localhost:4443
pause