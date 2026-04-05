REM Ignore this file, it's for cleaning up test tags in git

@echo off
setlocal enabledelayedexpansion

echo Fetching tags...

for /f "delims=" %%t in ('git tag') do (
    set "tag=%%t"

    REM Check if tag contains -test OR -temp OR -ci OR -rc
    echo !tag! | find "-test" >nul
    if !errorlevel! == 0 set "match=1"

    echo !tag! | find "-temp" >nul
    if !errorlevel! == 0 set "match=1"

    echo !tag! | find "-ci" >nul
    if !errorlevel! == 0 set "match=1"

    echo !tag! | find "-rc" >nul
    if !errorlevel! == 0 set "match=1"

    if defined match (
        echo Processing !tag!

        REM Take part before first "-"
        for /f "tokens=1 delims=-" %%a in ("!tag!") do (
            set "base=%%a"
        )

        echo New tag: !base!

        REM Delete old tag
        git tag -d !tag!

        REM Delete remote tag (optional)
        git push origin :refs/tags/!tag!

        REM Create new tag
        git tag !base!

        REM Push new tag
        git push origin !base!
    )

    set "match="
)

echo Done
pause