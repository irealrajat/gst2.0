; Custom NSIS installer script for BizGST Pro
; This file is included by electron-builder automatically

!macro customHeader
  !system "echo Building BizGST Pro installer..."
!macroend

!macro customInstall
  ; Create data directory for app data
  CreateDirectory "$APPDATA\BizGST Pro"
!macroend

!macro customUnInstall
  ; Optional: ask user to remove data on uninstall
  MessageBox MB_YESNO "Do you want to remove all BizGST Pro data (invoices, customers, etc)?" IDNO skip_data_removal
    RMDir /r "$APPDATA\BizGST Pro"
  skip_data_removal:
!macroend
