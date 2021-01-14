:: https://stackoverflow.com/questions/19835849/batch-script-iterate-through-arguments

@echo off
setlocal enabledelayedexpansion
set cdpath=%cd%

::slett og gjør klart folderet
rmdir /S /Q %appdata%\easycomp\compiled
mkdir %appdata%\easycomp\compiled
xcopy /E /I %appdata%\easycomp\.vscode %appdata%\easycomp\compiled\.vscode
copy %appdata%\easycomp\Makefile %appdata%\easycomp\compiled\Makefile

IF [%~1]==[] (GOTO ONLYMAIN) ELSE (GOTO RENAMEDMAIN)

:INCLUDEFILES
   ::echo INCLUDE-FILES
   set argCount=0
   for %%x in (%*) do (
      set /A argCount+=1
      set "argVec[!argCount!]=%%~x"
   )

   ::echo Number of processed arguments: %argCount%

   for /L %%i in (2,1,%argCount%) do (
      :: echo %%i- "!argVec[%%i]!"
      if exist "%cd%\!argVec[%%i]!" (
         copy "%cd%\!argVec[%%i]!" "%appdata%\easycomp\compiled\!argVec[%%i]!"
         echo exist
      ) else (
         echo [ERROR]: "%cd%\!argVac[%%i]!" does not exist. 
         GOTO DONE
      )
   )
   GOTO MAIN

:RENAMEDMAIN
   :: echo RENAMED-MAIN
   echo %cd%\%1
   if exist "%cd%\%1" (
      copy "%cd%\%1" "%appdata%\easycomp\compiled\main.cpp"
   ) else (
      echo [ERROR]: "%cd%\%1" does not exist
      GOTO DONE
   )
   GOTO INCLUDEFILES

:ONLYMAIN
   :: echo ONLY-MAIN
   if exist "%cd%\main.cpp" (
      copy "%cd%\main.cpp" "%appdata%\easycomp\compiled\main.cpp"
   ) else (
      echo [ERROR]: "%cd%\main.cpp" does not exist
      GOTO DONE
   )
   GOTO MAIN


:MAIN
   :: echo MAIN
   cd %appdata%\easycomp\compiled
   call "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
   nmake "DEBUG_BUILD=true" clearscreen clean debug.exe
   start %appdata%\easycomp\compiled\debug\debug.exe
   
   :: https://stackoverflow.com/questions/3215501/batch-remove-file-extension
   IF [%~1]==[] (
      copy "%appdata%\easycomp\compiled\debug\debug.exe" "%cdpath%\main.exe"
   ) ELSE (
      for %%f in ("%1") do copy "%appdata%\easycomp\compiled\debug\debug.exe" "%cdpath%\%%~nf.exe"
   )

:DONE
