# BizGST Pro 🧾
## GST Billing & Accounting Software — Windows Desktop App

## 📥 Download
Go to **Releases** tab → Download `BizGST-Pro-Setup-x.x.x.exe` (installer) or `BizGST-Pro-Portable-x.x.x.exe` (no install needed)

## 🏗️ File Structure
```
bizgst-pro/
├── index.html          ← Main app (React, all-in-one)
├── main.js             ← Electron desktop wrapper
├── package.json        ← Build config
├── installer.nsh       ← Installer customization
├── generate_icon.py    ← Auto icon generator
└── .github/workflows/deploy.yml  ← Auto builds .exe on push
```

## 🚀 Auto Build Flow
```
git push → GitHub Actions (Windows Server)
         → Generate icon → npm install
         → electron-builder → .exe
         → GitHub Release created ✅
```

## 💻 Run Locally
```bash
npm install
npm start          # dev mode
npm run build:win  # build .exe → dist/ folder
```

## 🔐 Default Password: BizGST@2024
To change: Open app → F12 console → run:
```js
crypto.subtle.digest('SHA-256', new TextEncoder().encode('NewPassword'))
  .then(b => console.log([...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')))
```
Replace `PASSWORD_HASH` in index.html with the output hash.
