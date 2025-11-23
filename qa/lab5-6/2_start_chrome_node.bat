@echo off
cls
echo ============================================
echo   STEP 2: Starting Chrome Node
echo ============================================
echo.

REM Find selenium jar
for %%f in (selenium-server*.jar) do set JAR=%%f

if not defined JAR (
    echo ERROR: selenium-server jar not found!
    pause
    exit /b 1
)

echo This node will connect to: http://localhost:4444
echo Browser: Chrome only
echo.
echo Make sure Hub is running first!
echo.
echo Press Ctrl+C to stop node
echo ============================================
echo.

java -jar %JAR% node ^
  --hub http://localhost:4444 ^
  --host localhost ^
  --port 5555 ^
  --detect-drivers true ^
  --driver-implementation chrome

pause