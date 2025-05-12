---

# 📘 ArchiSteamFarm (ASF) Installation Guide on Ubuntu (No Docker)

---

## 📌 Prerequisites

Ensure your system has:

* Ubuntu 22.04 or newer
* `wget`, `unzip`, and `screen` (optional)
* Internet access

---

## ✅ Step 1: Install .NET Runtime (Only needed for `.dll` builds – *skip for standalone*)

> If you're using the **standalone ASF binary**, you can skip this step.

```bash
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update
sudo apt install -y dotnet-runtime-8.0
```

---

## ✅ Step 2: Download ASF Standalone Binary

```bash
cd ~
mkdir -p ~/ssd-downloads/ASF
cd ~/ssd-downloads/ASF
wget https://github.com/JustArchiNET/ArchiSteamFarm/releases/latest/download/ASF-linux-x64.zip
unzip ASF-linux-x64.zip
rm ASF-linux-x64.zip
chmod +x ArchiSteamFarm
```

---

## ✅ Step 3: Configure ASF

Create the configuration folder:

```bash
mkdir -p config
```

### 🔹 ASF.json

```bash
nano config/ASF.json
```

Paste:

```json
{
  "CurrentCulture": "en-US",
  "IPCHost": "0.0.0.0"
}
```

### 🔹 MyBot.json

```bash
nano config/MyBot.json
```

Paste:

```json
{
  "Enabled": true,
  "Username": "your_steam_username",
  "Password": "your_steam_password",
  "GamesPlayedWhileIdle": [730],
  "FarmingOrders": [],
  "FarmingPreferences": 0
}
```

> Replace with your actual credentials. `730` = CS\:GO AppID.

---

## ✅ Step 4: Run ASF

To run ASF interactively:

```bash
./ArchiSteamFarm
```

You’ll be prompted for a Steam Guard code on first login.

---

## ✅ Step 5: Run ASF in Background (Optional)

Use `screen`:

```bash
sudo apt install screen
screen -S asf
./ArchiSteamFarm
```

Detach: `Ctrl+A` then `D`
Reattach: `screen -r asf`

---

## ✅ Step 6: Enable ASF as a systemd Service

Create service file:

```bash
sudo nano /etc/systemd/system/asf.service
```

Paste:

```ini
[Unit]
Description=ArchiSteamFarm Bot
After=network.target

[Service]
Type=simple
User=harsh
WorkingDirectory=/home/harsh/ssd-downloads/ASF
ExecStart=/home/harsh/ssd-downloads/ASF/ArchiSteamFarm
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Reload and enable:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable asf
sudo systemctl start asf
```

---

## ✅ Step 7: Verify Service

Check status:

```bash
systemctl status asf
```

Check logs:

```bash
journalctl -u asf -f
```

---

## 🌐 Access Web UI

Visit this in your browser:

```
http://<your-server-ip>:1242
```

---

## ✅ Notes

* Session is saved after login, so re-entering Steam Guard code is not needed unless your session expires.
* You can manage ASF via the Web UI after login.
* To change your config, edit files inside the `config/` folder and restart the service:

  ```bash
  sudo systemctl restart asf
  ```

---
