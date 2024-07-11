# Installing Home Assistant on Ubuntu Server

This guide covers the steps to install Home Assistant on an Ubuntu server, ensuring the service runs smoothly and is accessible over the network.

## Step 1: Update Your System
First, ensure your system is up to date to avoid any compatibility issues.
```bash
# Update the package list
sudo apt update

# Upgrade all installed packages to their latest versions
sudo apt upgrade -y
```

## Step 2: Install Dependencies
Home Assistant requires Python and some additional packages.
```bash
# Install Python 3, the Python 3 virtual environment package, and pip
sudo apt install -y python3 python3-venv python3-pip
```

## Step 3: Create a Home Assistant User
For security reasons, it's best to run Home Assistant under its own user.
```bash
# Create a new user called 'homeassistant'
sudo useradd -rm homeassistant

# Create a directory for Home Assistant's files
sudo mkdir /srv/homeassistant

# Change the ownership of the directory to the new 'homeassistant' user
sudo chown homeassistant:homeassistant /srv/homeassistant
```

## Step 4: Create and Activate a Virtual Environment
Switch to the `homeassistant` user, create a virtual environment, and activate it.
```bash
# Switch to the 'homeassistant' user
sudo -u homeassistant -H -s

# Navigate to the Home Assistant directory
cd /srv/homeassistant

# Create a virtual environment in the current directory
python3 -m venv .

# Activate the virtual environment
source bin/activate
```

## Step 5: Install Home Assistant
With the virtual environment activated, install Home Assistant using pip.
```bash
# Install the wheel package (helps in installing other packages)
pip install wheel

# Install Home Assistant
pip install homeassistant
```

## Step 6: Create a Systemd Service
Exit the virtual environment and create a systemd service to manage Home Assistant.
```bash
# Exit the virtual environment
exit

# Open a new systemd service file for Home Assistant
sudo nano /etc/systemd/system/home-assistant@homeassistant.service
```

Add the following content to the file:
```ini
[Unit]
Description=Home Assistant
After=network-online.target

[Service]
Type=simple
User=homeassistant
ExecStart=/srv/homeassistant/bin/hass -c "/home/homeassistant/.homeassistant"

[Install]
WantedBy=multi-user.target
```
Save the file and exit the editor.

## Step 7: Start and Enable the Service
Reload systemd to recognize the new service, start it, and enable it to run on boot.
```bash
# Reload systemd to recognize the new service file
sudo systemctl --system daemon-reload

# Start the Home Assistant service
sudo systemctl start home-assistant@homeassistant

# Enable the service to start automatically on boot
sudo systemctl enable home-assistant@homeassistant
```

## Step 8: Open Port 8123 in the Firewall
Ensure that the firewall allows traffic on port 8123.
```bash
# Allow traffic on port 8123
sudo ufw allow 8123

# Check the firewall status to confirm the rule was added
sudo ufw status
```

## Step 9: Access Home Assistant
Home Assistant should now be running and accessible. You can access it from a web browser on your local network at:
```
http://192.168.1.101:8123
```

## Troubleshooting
### Check Service Status
If you encounter any issues, check the status of the Home Assistant service.
```bash
sudo systemctl status home-assistant@homeassistant
```

### View Logs
To get more details on any errors, view the logs.
```bash
sudo journalctl -fu home-assistant@homeassistant
```

### Common Issues
- **Network Connectivity**: Ensure your server is correctly connected to the network and that the IP address is correct.
- **Firewall**: Make sure the firewall is not blocking necessary ports.
- **Database Warnings**: If you see warnings related to the SQLite database, stop Home Assistant and perform a database check:
  ```bash
  sudo systemctl stop home-assistant@homeassistant
  sqlite3 /home/homeassistant/.homeassistant/home-assistant_v2.db "PRAGMA integrity_check;"
  sudo systemctl start home-assistant@homeassistant
  ```

### Local Connection Test
To verify Home Assistant is running, you can test the connection locally from the server itself using `curl`.
```bash
curl http://localhost:8123
```

### Clear Browser Cache
If you have trouble accessing Home Assistant, clear your browser cache or try a different browser or an incognito window.
