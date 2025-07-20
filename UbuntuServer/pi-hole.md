---

# ✅ Pi-hole + Tailscale Installation Log Summary

**Host:** `harsh-server`
**OS:** Ubuntu 24.04
**User:** `harsh`
**Pi-hole Web UI:** `http://192.168.1.101/admin`
**DNS IPs:** `192.168.1.101` (IPv4), `fd7a:115c:a1e0::a501:5759` (IPv6)
**Web UI Password:** `xxxxxx` (You can change it with `pihole -a -p` or `sudo pihole setpassword` )

---

## ⚙️ Step-by-Step Summary

### 1. ✅ UFW Firewall Installed

```bash
sudo apt-get install ufw -y
```

* UFW (Uncomplicated Firewall) was already installed and up to date.
* You can enable and configure it using:

  ```bash
  sudo ufw enable
  sudo ufw allow 22/tcp   # Allow SSH
  ```

---

### 2. ✅ Tailscale Activated (Without Accepting DNS)

```bash
sudo tailscale up --accept-dns=false
```

* This ensures Tailscale doesn’t override your system DNS settings.
* Your server is now securely connected to your Tailnet.

---

### 3. ✅ Pi-hole Installed with OS Check Bypassed

```bash
curl -sSL https://install.pi-hole.net | PIHOLE_SKIP_OS_CHECK=true sudo -E bash
```

#### Configuration Summary:

* **Interface Used:** `tailscale0`
* **IPv4 Address:** `192.168.1.101`
* **IPv6 ULA Address:** `fd7a:115c:a1e0::a501:5759`
* **Upstream DNS:** `127.0.0.1#5335` (for Unbound resolver)
* **Privacy Mode:** `Show everything` *(default selected = level 0)*

---

### 4. 📁 Repositories Cloned

* Core: [`pi-hole/pi-hole`](https://github.com/pi-hole/pi-hole)
* Web Admin: [`pi-hole/web`](https://github.com/pi-hole/web)
* Both were successfully cloned to:

  * `/etc/.pihole`
  * `/var/www/html/admin`

---

### 5. 👥 User and Group Created

* Group: `pihole`
* User: `pihole`

---

### 6. 🧠 FTL (Fast Telemetry Lookup) Installed and Enabled

* Architecture detected: `x86_64`
* FTL service enabled to **auto-start on boot**
* Systemd DNS stub listener (`systemd-resolved`) was **disabled** to avoid conflicts

---

### 7. 📚 Blocklists and Gravity Database

* Blocklist Used: [StevenBlack Unified Hosts List](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts)
* Domains Blocked: **221,445**
* Gravity database created and optimized
* Database swap successful
* Logging: Enabled
* Neutrino emissions detected (Pi-hole's cheeky term for success)

---

### 8. 🧪 DNS Verification

* DNS resolution was confirmed to be working locally after installation.
* You can test DNS using:

  ```bash
  nslookup google.com 127.0.0.1
  nslookup doubleclick.net 127.0.0.1
  ```

---

### 9. 🔐 Access Details

| Feature         | URL / Command                                            |
| --------------- | -------------------------------------------------------- |
| Web UI          | [http://192.168.1.101/admin](http://192.168.1.101/admin) |
| DNS IPv4        | 192.168.1.101                                            |
| DNS IPv6        | fd7a:115c\:a1e0::a501:5759                               |
| Admin Password  | `xxxxxxxx`                                               |
| Change Password | `pihole -a -p`                                           |
| Logs            | `/etc/pihole/install.log`                                |

---

### 10. 🔁 Post-Install Suggestions

#### 🔧 Change Privacy Mode (Optional)

Current mode: `Show everything` (level 0)
Recommended: `Anonymous mode` for better privacy
Change via:

```bash
Settings > Privacy > Anonymous mode
```

---

## 📌 Next Steps

### ✅ \[Optional] Install Unbound for Private DNS Resolution

Follow this part of your original guide:

```bash
sudo apt install unbound -y
```

Then configure `/etc/unbound/unbound.conf.d/pi-hole.conf` as per your Unbound section.

---

### ✅ Configure Firewall to Allow DNS and Web from Tailnet

```bash
sudo ufw allow from 192.168.1.0/24 to any port 53
sudo ufw allow from 100.64.0.0/10 to any port 53
sudo ufw allow from 192.168.1.0/24 to any port 80
sudo ufw allow from 100.64.0.0/10 to any port 80
sudo ufw allow from 192.168.1.0/24 to any port 443
sudo ufw allow from 100.64.0.0/10 to any port 443
sudo ufw reload
```

---

### ✅ Tailscale Admin DNS Settings

* Go to: [https://login.tailscale.com/admin/dns](https://login.tailscale.com/admin/dns)
* Add **Nameserver**: `100.x.x.x` (Tailscale IP of this server)
* Enable: **Override local DNS**

---

## 🛡️ Security Notes

* Web UI only accessible via firewall-allowed networks (local + Tailnet)
* DNS resolution blocked from public internet
* Password protected web interface
* Logging enabled (can be reduced for privacy)
* Auto-start on boot: enabled

---
