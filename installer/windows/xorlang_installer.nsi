; XorLang v2.0.0 Windows Installer
; NSIS Script for creating Windows installer

!define APP_NAME "XorLang"
!define APP_VERSION "2.0.0"
!define APP_PUBLISHER "Ali Jafari"
!define APP_EXE "xorlang.exe"
!define APP_IDE_EXE "xorlang-ide.exe"
!define APP_URL "https://github.com/Mr-Ali-Jafari/Xorlang"

; Include modern UI
!include "MUI2.nsh"
!include "FileFunc.nsh"

; General
Name "${APP_NAME} ${APP_VERSION}"
OutFile "XorLang-${APP_VERSION}-Setup.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKCU "Software\${APP_NAME}" ""

; Request application privileges
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\..\src\xorlang\x.ico"
!define MUI_UNICON "..\..\src\xorlang\x.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\..\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "MainApplication" SecMain
    SectionIn RO
    SetOutPath "$INSTDIR"
    
    ; Copy main executable
    File "..\..\dist\${APP_EXE}"
    
    ; Copy IDE executable
    File "..\..\dist\${APP_IDE_EXE}"
    
    ; Copy standard library
    SetOutPath "$INSTDIR\stdlib"
    File /r "..\..\src\xorlang\stdlib\*.*"
    
    ; Copy documentation
    SetOutPath "$INSTDIR\docs"
    File "..\..\README.md"
    File "..\..\CHANGELOG.md"
    File "..\..\PERFORMANCE_OPTIMIZATIONS.md"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Registry information for add/remove programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME} ${APP_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "QuietUninstallString" "$\"$INSTDIR\Uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation" "$\"$INSTDIR$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$\"$INSTDIR\${APP_EXE}$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "VersionMajor" 2
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "VersionMinor" 0
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    
    ; Get the size of the installed files
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "EstimatedSize" "$0"
SectionEnd

Section "Start Menu Shortcuts" SecStartMenu
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME} IDE.lnk" "$INSTDIR\${APP_IDE_EXE}" "" "$INSTDIR\${APP_IDE_EXE}" 0
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
SectionEnd

Section "Desktop Shortcuts" SecDesktop
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
    CreateShortCut "$DESKTOP\${APP_NAME} IDE.lnk" "$INSTDIR\${APP_IDE_EXE}" "" "$INSTDIR\${APP_IDE_EXE}" 0
SectionEnd

Section "Add to PATH" SecPath
    ; Add to system PATH
    EnVar::SetHKLM
    EnVar::AddValue "Path" "$INSTDIR"
SectionEnd

; Uninstaller Section
Section "Uninstall"
    ; Remove files and uninstaller
    Delete "$INSTDIR\${APP_EXE}"
    Delete "$INSTDIR\${APP_IDE_EXE}"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove directories
    RMDir /r "$INSTDIR\stdlib"
    RMDir /r "$INSTDIR\docs"
    RMDir "$INSTDIR"
    
    ; Remove start menu items
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME} IDE.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    
    ; Remove desktop shortcuts
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$DESKTOP\${APP_NAME} IDE.lnk"
    
    ; Remove from PATH
    EnVar::SetHKLM
    EnVar::DeleteValue "Path" "$INSTDIR"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKCU "Software\${APP_NAME}"
SectionEnd

; Descriptions
LangString DESC_SecMain ${LANG_ENGLISH} "Install ${APP_NAME} ${APP_VERSION} (required)"
LangString DESC_SecStartMenu ${LANG_ENGLISH} "Create Start Menu shortcuts"
LangString DESC_SecDesktop ${LANG_ENGLISH} "Create Desktop shortcuts"
LangString DESC_SecPath ${LANG_ENGLISH} "Add ${APP_NAME} to system PATH"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecPath} $(DESC_SecPath)
!insertmacro MUI_FUNCTION_DESCRIPTION_END
