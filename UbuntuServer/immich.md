---
https://immich.app/docs/overview/quick-start
---

# 📸 Immich Self-Hosting Setup — Local Ubuntu Server

**Server IP:** `192.168.1.101`
**Server OS:** `Ubuntu 24.04.2 LTS`
**Docker-based deployment**
**Storage Path:** Customisable via `.env` file

---

## 📦 1. Installation Instructions

### A. Install Required Dependencies

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin curl git
sudo systemctl enable docker
sudo systemctl start docker
```

---

### B. Install Immich via Official Script

This is the **recommended quick method**:

```bash
curl -o- https://raw.githubusercontent.com/immich-app/immich/main/install.sh | bash
```

* This will download the latest Docker Compose config into `~/immich-app`
* Pulls containers and starts Immich

---

## 🚀 2. Running Immich

Once installed, go to the install directory:

```bash
cd ~/immich-app
```

To bring up Immich:

```bash
docker compose up -d
```

Open in browser:

```
http://192.168.1.101:2283
```

---

## ⚙️ 3. Configuration

To change settings like:

* Upload/backup storage path
* Database and Redis configuration
* Web port (default `2283`)
* Timezone

### Steps:

1. **Stop containers**:

   ```bash
   docker compose down
   ```

2. **Edit the `.env` file**:

   ```bash
   nano .env
   ```

   Suggested edits:

   ```dotenv
   UPLOAD_LOCATION=/mnt/harddisk/immich-uploads
   DB_DATA_LOCATION=/mnt/harddisk/immich-db
   IMMICH_WEB_PORT=2283
   ```

3. **Restart Immich**:

   ```bash
   docker compose up --remove-orphans -d
   ```

---

## 🔄 4. Updating Immich

Whenever you want to update Immich to the latest version:

```bash
cd ~/immich-app
docker compose down
docker compose pull
docker compose up -d
```

To verify:

```bash
docker compose ps
```

---

## 🧠 5. Tips and Best Practices

### Storage Best Practices

* Use **SSD storage** for faster access to uploads and DB
* Store `UPLOAD_LOCATION` and `DB_DATA_LOCATION` on separate disk (e.g., `/mnt/harddisk`)
* Regularly back up:

  * Postgres volume
  * Uploads directory

### Access Immich on Local Network

Check your server’s IP:

```bash
hostname -I
```

Visit in browser:

```
http://<server-ip>:2283
```

---

## 🔒 6. \[Optional] Setup HTTPS + Domain

To expose Immich with HTTPS using Nginx:

1. Install Nginx:

   ```bash
   sudo apt install nginx
   ```

2. Point a domain to your server’s public IP (if any)

3. Use [Caddy](https://caddyserver.com/) or [Let's Encrypt](https://certbot.eff.org/) to get free SSL

Let me know if you want the complete reverse proxy setup.

---

## 🛠 7. Useful Docker Commands

```bash
# Start Immich
docker compose up -d

# Stop Immich
docker compose down

# View logs
docker compose logs -f

# Restart all containers
docker compose restart

# Show container status
docker compose ps
```

---

## 🗂 8. Folder Structure

If installed via script, your folder looks like:

```
~/immich-app/
├── docker-compose.yml
├── .env
├── README.md
└── volumes/
    ├── uploads/
    ├── postgres/
    └── model-cache/
```

---

## 📅 9. \[Optional] Auto-Update with Watchtower

Install Watchtower to auto-update Immich containers:

```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --cleanup \
  --interval 86400
```

---

## ✅ Quick Reference Summary

| Task          | Command / URL                                   |
| ------------- | ----------------------------------------------- |
| Access Immich | `http://192.168.1.101:2283`                     |
| Start Immich  | `docker compose up -d`                          |
| Stop Immich   | `docker compose down`                           |
| Update Immich | `docker compose pull && docker compose up -d`   |
| Change config | Edit `.env`, restart with `up --remove-orphans` |
| View logs     | `docker compose logs -f`                        |
| Server IP     | `hostname -I`                                   |

---
