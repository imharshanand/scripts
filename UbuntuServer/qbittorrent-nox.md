Guide to use qBittorrent on an Ubuntu server, including starting it in daemon mode, accessing the Web UI, setting a permanent password, and configuring auto shutdown after downloads complete.

```markdown
# qBittorrent Setup on Ubuntu Server

This guide provides detailed steps to set up qBittorrent on an Ubuntu Server, including running it in daemon mode, accessing the Web UI, setting a permanent password, and configuring auto shutdown after downloads complete.

## Prerequisites

- Ubuntu Server 22.04
- Basic knowledge of command-line operations
- Access to the server (via SSH or direct login)

## Installation

1. **Update the System:**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install qBittorrent-nox:**
   `qbittorrent-nox` is the command-line version of qBittorrent, suitable for servers without a graphical user interface.
   ```bash
   sudo apt install qbittorrent-nox -y
   ```

## Running qBittorrent in Daemon Mode

1. **Start qBittorrent:**
   ```bash
   qbittorrent-nox --webui-port=8080
   ```

2. **Accept Legal Notice:**
   - When prompted, press `y` to accept and continue.

## Accessing the Web UI

1. **Open your web browser and navigate to:**
   ```
   http://<server-ip>:8080
   ```
   Replace `<server-ip>` with the actual IP address of your server. If you are running the browser on the same machine as the server, you can use `http://localhost:8080`.

2. **Log In:**
   - Username: `admin`
   - Temporary Password: Provided in the terminal (e.g., `Q5UkWAfSC`)

## Setting a Permanent Password

1. **Navigate to Preferences:**
   - In the Web UI, go to the `Preferences` section (usually accessible via a settings icon or menu).

2. **Set a New Password:**
   - Go to the `Web UI` tab.
   - Change the password to something secure and memorable.
   - Save the changes.

## Configuring Auto Shutdown After Downloads Complete

1. **Open Preferences in the Web UI:**
   - Go to the `Preferences` section.

2. **Navigate to Downloads Tab:**
   - Check the option `Run external program on torrent completion`.

3. **Set Shutdown Command:**
   - Enter the following command to shut down the system after all torrents complete:
     ```bash
     shutdown -h now
     ```

## Summary

By following the above steps, you can install and configure qBittorrent on your Ubuntu Server. This setup includes running qBittorrent in daemon mode, accessing and configuring the Web UI, setting a secure password, and enabling system shutdown after all downloads are complete.

## Troubleshooting

- **Cannot access the Web UI:**
  - Ensure that the port `8080` is open in your firewall settings.
  - Verify that qBittorrent is running by checking the process list:
    ```bash
    ps aux | grep qbittorrent-nox
    ```

- **Changing Web UI Port:**
  - If `8080` is already in use, you can specify a different port when starting qBittorrent:
    ```bash
    qbittorrent-nox --webui-port=<new-port>
    ```

- **Stopping qBittorrent Daemon:**
  - Find the PID of qBittorrent:
    ```bash
    ps aux | grep qbittorrent-nox
    ```
  - Kill the process using its PID:
    ```bash
    kill <PID>
    ```

To configure qBittorrent to start automatically when your Ubuntu server boots, you can create a systemd service. This will ensure that qBittorrent runs in daemon mode on startup.

Here are the steps to create a systemd service for qBittorrent:

### Step 1: Create the Systemd Service File

1. Open a terminal on your Ubuntu server.
2. Create a new service file for qBittorrent:
   ```bash
   sudo nano /etc/systemd/system/qbittorrent.service
   ```

3. Add the following content to the file:

   ```ini
   [Unit]
   Description=qBittorrent Command Line Client
   After=network.target

   [Service]
   User=your_username
   ExecStart=/usr/bin/qbittorrent-nox --webui-port=8080
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

   Replace `your_username` with the username you use to log in to your server.

### Step 2: Enable the Service

1. Reload the systemd daemon to recognize the new service:
   ```bash
   sudo systemctl daemon-reload
   ```

2. Enable the qBittorrent service to start on boot:
   ```bash
   sudo systemctl enable qbittorrent
   ```

3. Start the qBittorrent service immediately:
   ```bash
   sudo systemctl start qbittorrent
   ```

### Step 3: Verify the Service

1. Check the status of the qBittorrent service to ensure it is running:
   ```bash
   sudo systemctl status qbittorrent
   ```

   You should see output indicating that the service is active and running.

### Full Example

Here is the full set of commands to run on your Ubuntu server:

```bash
# Create the systemd service file
sudo nano /etc/systemd/system/qbittorrent.service

# Add the following content to the file
# [Unit]
# Description=qBittorrent Command Line Client
# After=network.target
#
# [Service]
# User=your_username
# ExecStart=/usr/bin/qbittorrent-nox --webui-port=8080
# Restart=on-failure
#
# [Install]
# WantedBy=multi-user.target

# Save and exit the file

# Reload the systemd daemon
sudo systemctl daemon-reload

# Enable the qBittorrent service to start on boot
sudo systemctl enable qbittorrent

# Start the qBittorrent service immediately
sudo systemctl start qbittorrent

# Check the status of the qBittorrent service
sudo systemctl status qbittorrent
```

By following these steps, qBittorrent will automatically start in daemon mode whenever your Ubuntu server boots up. You can manage the service using systemd commands like `start`, `stop`, `restart`, and `status`.


To manage `qbittorrent-nox` with `systemctl`, you need to create a systemd service file for it. Here are the steps to do this:

1. **Create a systemd Service File**:
   Open a text editor to create a new service file. For example, using `nano`:

   ```bash
   sudo nano /etc/systemd/system/qbittorrent-nox.service
   ```

2. **Add Service Configuration**:
   Add the following content to the file:

   ```ini
   [Unit]
   Description=qBittorrent-nox
   After=network.target

   [Service]
   User=harsh_server
   ExecStart=/usr/bin/qbittorrent-nox --webui-port=8080
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

   Make sure to replace `harsh_server` with the correct username if it's different. Adjust the path to `qbittorrent-nox` if it is not located in `/usr/bin/`.

3. **Reload Systemd Daemon**:
   After creating the service file, reload the systemd daemon to recognize the new service:

   ```bash
   sudo systemctl daemon-reload
   ```

4. **Start and Enable the Service**:
   Start the `qbittorrent-nox` service and enable it to start on boot:

   ```bash
   sudo systemctl start qbittorrent-nox
   sudo systemctl enable qbittorrent-nox
   ```

5. **Verify the Service**:
   Check the status to ensure it is running:

   ```bash
   sudo systemctl status qbittorrent-nox
   ```

Now you can stop the service using:

```bash
sudo systemctl stop qbittorrent-nox
```

And start it again using:

```bash
sudo systemctl start qbittorrent-nox
```

With this setup, `qbittorrent-nox` will be managed by `systemd` and can be controlled with `systemctl` commands.
