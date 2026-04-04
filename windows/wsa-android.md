
---

# 📦 Magisk + WSA + LSPosed + Pixelify Setup (Windows 10)

> Fully working Windows Subsystem for Android (WSA) setup with Magisk root, LSPosed, and Pixelify for Google Photos — tested on Windows 10.

---

## ⚠️ Disclaimer

* This setup uses **patched WSA builds** (not officially supported by Microsoft)
* Pixel spoofing may break due to Google updates
* WSA is planned to be discontinued by Microsoft
* Use at your own risk

---

# 🧾 System Information

```bash
Windows 10 Pro
Version: 22H2
OS Build: 19045.6456
```

---

# 🧾 Requirements

* Windows 10 22H2 (Build 19045+)
* Virtualization enabled (BIOS)
* Windows Features:

  * Virtual Machine Platform
  * Windows Hypervisor Platform
* Developer Mode enabled

---

# 🧾 Setup Overview

```text
Windows 10
   ↓
WSA (Android 13)
   ↓
Magisk (Root)
   ↓
Zygisk
   ↓
LSPosed
   ↓
Pixelify (Google Photos spoof)
```

---

# 🧾 1. Install ADB (Platform Tools)

Download:
👉 [https://developer.android.com/tools/releases/platform-tools](https://developer.android.com/tools/releases/platform-tools)

Extract to:

```bash
C:\adb
```

Verify:

```bash
adb version
```

---

# 🧾 2. Install WSA (Patched for Windows 10)

### 📦 Package Used

```text
WSA_2407.40000.4.0_x64_Release-Nightly-with-magisk-30.6-stable-GApps-13.0_Windows_10.7z
```

### 📥 Source

👉 [https://github.com/MustardChef/WSABuilds](https://github.com/MustardChef/WSABuilds)

---

### ⚙️ Installation

```bash
1. Extract using 7-Zip
2. Open extracted folder
3. Run Run.bat
```

---

### ⚙️ WSA Settings

* Developer Mode: ✅ Enabled
* Subsystem: Running

---

# 🧾 3. Connect ADB

```bash
adb connect 127.0.0.1:58526
adb devices
```

Expected:

```text
127.0.0.1:58526 device
```

---

# 🧾 4. Magisk Setup

### Version

```text
Magisk: 30.6
Magisk App: 30.7
```

### Configuration

* Zygisk: ✅ Enabled
* DenyList: Optional

---

# 🧾 5. Install LSPosed

### Module Info

```text
Zygisk - LSPosed v1.9.2 (7024)
```

---

### Install Steps

1. Open **Magisk**
2. Go to **Modules**
3. Install LSPosed (zygisk version)
4. Reboot WSA

---

### Verify

* LSPosed: ✅ Active
* Zygisk: ✅ Active

---

# 🧾 6. Install Pixelify (Google Photos)

### Module

```text
Pixelify GPhotos v4.1
```

### Source

👉 [https://github.com/BaltiApps/Pixelify-Google-Photos](https://github.com/BaltiApps/Pixelify-Google-Photos)

---

### Setup

1. Install APK:

```bash
adb install pixelify.apk
```

2. Open **LSPosed**

3. Enable Pixelify for:

   * Google Photos
   * Google Play Services

4. Reboot:

```bash
adb reboot
```

---

# 🧾 7. Installed Modules

| Module            | Version  |
| ----------------- | -------- |
| GApps for WSA     | v33 (16) |
| WSA Customization | v1 (16)  |
| LSPosed (Zygisk)  | v1.9.2   |
| Pixelify GPhotos  | v4.1     |

---

# 🧾 8. Android Environment

```text
Android Version: 13
```

### Installed Apps

* Google Play Store
* Google Play Services
* Magisk
* Amazon Appstore

---

# 🧾 9. File Structure

```text
Downloads/
├── platform-tools/
├── WSA_2407.../
├── WSA_2311... (unused)
```

---

# 🧾 10. Backup (IMPORTANT)

### 🔴 Backup Android System

```bash
C:\Users\<user>\AppData\Local\Packages\
MicrosoftCorporationII.WindowsSubsystemForAndroid_*\LocalState\userdata.vhdx
```

---

### 🔴 Backup Installation Folder

```bash
WSA_2407... folder
```

---

# 🧾 11. Restore Setup

```bash
1. Reinstall WSA
2. Replace userdata.vhdx
3. Start WSA
```

---

# 🧾 12. Known Issues

* Pixelify may stop working after:

  * Google Photos update
  * Google Play Services update

---

# 🧾 13. Stability Tips

* Disable auto-update for:

  * Google Photos
  * Google Play Services

* Keep WSA running in background

---

# 🧾 14. Status

| Component | Status       |
| --------- | ------------ |
| WSA       | ✅ Working    |
| Magisk    | ✅ Working    |
| Zygisk    | ✅ Enabled    |
| LSPosed   | ✅ Active     |
| Pixelify  | ⚠️ May break |
| ADB       | ✅ Connected  |

---

# 🚀 Credits

* LSPosed Team
* MustardChef (WSABuilds)
* BaltiApps (Pixelify)

---

# ⭐ Final Notes

This setup provides a **fully rooted Android environment on Windows 10**, with:

* Google Play support
* LSPosed framework
* Pixel spoofing capability

---
