set /p CURRENT_VERSION=<version.txt

echo Current version is: %CURRENT_VERSION%
pause
if "%CURRENT_VERSION%"=="0.1" (
    echo Version is up to date.
) else (
    echo Version mismatch. Pulling from git...
    start pull.bat
)
pause