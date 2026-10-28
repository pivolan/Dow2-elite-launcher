; Elite Launcher installer additions (included by Tauri's installer.nsi before its pages).
; The launcher must not be installed into the Dawn of War II folder: files of the launcher there break the game
; (crash near the end of a match load was reported with the portable build in the game folder).

!define MUI_DIRECTORYPAGE_TEXT_TOP "Установите лаунчер в любую папку, но НЕ в папку с Dawn of War II (там, где DOW2.exe) — иначе игра может падать. Папку игры лаунчер найдёт сам.$\r$\n$\r$\nInstall the launcher anywhere EXCEPT the Dawn of War II folder (where DOW2.exe is) - the game may crash otherwise. The launcher finds the game by itself."

; Next is disabled while the chosen folder is the game folder or inside it
Function .onVerifyInstDir
  IfFileExists "$INSTDIR\DOW2.exe" bad
  IfFileExists "$INSTDIR\..\DOW2.exe" bad
  IfFileExists "$INSTDIR\..\..\DOW2.exe" bad
  Return
  bad:
    Abort
FunctionEnd
