@echo off
cls
echo ============================================
echo   STEP 3: Starting Firefox Node
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
echo Browser: Firefox only
echo Port: 5556 (different from Chrome node)
echo.
echo Make sure Hub is running first!
echo.
echo Press Ctrl+C to stop node
echo ============================================
echo.

java -jar %JAR% node ^
  --hub http://localhost:4444 ^
  --host localhost ^
  --port 5556 ^
  --detect-drivers true ^
  --driver-implementation firefox

pause