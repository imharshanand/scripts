Sure! Here is a more detailed README file for your GitHub repository:

```markdown
# Ubuntu Server Triple Boot Configuration

This repository contains detailed instructions and configurations for setting up a triple boot system with Ubuntu 24.04 LTS Desktop, Ubuntu 24.04 Server, and Windows 11.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
  - [Preparing Installation Media](#preparing-installation-media)
  - [Installing Ubuntu 24.04 LTS Desktop](#installing-ubuntu-2404-lts-desktop)
  - [Installing Windows 11](#installing-windows-11)
  - [Installing Ubuntu 24.04 Server](#installing-ubuntu-2404-server)
  - [Configuring GRUB](#configuring-grub)
- [Network Configuration](#network-configuration)
- [Password Reset](#password-reset)
- [Listing Users](#listing-users)
- [SSH Connection](#ssh-connection)
- [GRUB Configuration](#grub-configuration)
- [Authors](#authors)
- [License](#license)

## Overview

This guide provides step-by-step instructions for setting up a triple boot system with Ubuntu 24.04 LTS Desktop, Ubuntu 24.04 Server, and Windows 11. It includes network configuration, password reset, listing users, SSH connection setup, and GRUB configuration.

## Prerequisites

- USB drives for installation media.
- ISO files for Ubuntu 24.04 LTS, Ubuntu 24.04 Server, and Windows 11.
- A computer with sufficient disk space for a triple boot setup.
- Basic understanding of partitioning and operating system installation.

## Installation Steps

### Preparing Installation Media

1. **Create Bootable USB Drives**:
   - Use tools like [Rufus](https://rufus.ie/) (Windows) or `dd` (Linux) to create bootable USB drives for Ubuntu and Windows.
   - Example command for `dd`:
     ```bash
     sudo dd if=/path/to/ubuntu.iso of=/dev/sdX bs=4M status=progress && sync
     ```
     Replace `/path/to/ubuntu.iso` with the path to your ISO file and `/dev/sdX` with the USB drive device.

### Installing Ubuntu 24.04 LTS Desktop

1. **Boot from USB**:
   - Insert the USB drive and boot from it. You may need to access the BIOS/UEFI settings to change the boot order.
2. **Follow Installation Steps**:
   - Complete the installation process, selecting the appropriate partition for Ubuntu Desktop. Set up the root password and create your user account.

### Installing Windows 11

1. **Boot from USB**:
   - Insert the Windows USB drive and boot from it. Again, you may need to change the boot order in the BIOS/UEFI settings.
2. **Follow Installation Steps**:
   - Complete the installation process, ensuring Windows is installed on a different partition from Ubuntu.

### Installing Ubuntu 24.04 Server

1. **Boot from USB**:
   - Insert the USB drive and boot from it.
2. **Network Configuration**:
   - When prompted to configure the network, select `wlan0` to connect to WiFi. Enter the SSID and password when prompted.
3. **Storage Configuration**:
   - Select partition 7 (145.072G) for the root filesystem (`/`).
   - Select partition 3 on WDC (287.221G) for additional storage (`/mnt/storage`).

### Configuring GRUB

1. **Edit GRUB Configuration**:
   - Open the GRUB configuration file using `nano` or your preferred text editor:
     ```bash
     sudo nano /etc/default/grub
     ```
   - Modify the following lines to ensure the GRUB menu is displayed and that it can detect other operating systems:
     ```plaintext
     GRUB_TIMEOUT_STYLE=menu
     GRUB_TIMEOUT=5
     ```
   - Save and exit the file.
2. **Update GRUB**:
   ```bash
   sudo update-grub
   ```

## Network Configuration

To connect to WiFi during the installation of Ubuntu Server, follow these steps:

1. **Select the WiFi Interface**:
   - In the network configuration screen, you should see the `wlan0` interface listed. Use the arrow keys to highlight it.

2. **Enable the WiFi Interface**:
   - Press `Enter` to select the `wlan0` interface. This will bring up additional options.

3. **Connect to a WiFi Network**:
   - You should now see options to connect to a WiFi network. Follow these steps:
     - Choose "Configure network" for the `wlan0` interface.
     - It will scan for available WiFi networks. Select your WiFi network from the list.
     - Enter the WiFi password when prompted.

4. **Continue with Installation**:
   - Once connected, the installer should proceed with the installation process, utilizing the WiFi connection for network access and updates.

If the installer does not automatically scan for WiFi networks, you may need to manually enter the network information:

1. **Manual Configuration**:
   - If prompted, enter the SSID (network name) and the security type (e.g., WPA2).
   - Enter the WiFi password.

2. **Verify Connection**:
   - Ensure that the WiFi connection is established and that the `wlan0` interface shows as connected.

3. **Proceed**:
   - Once connected, continue with the rest of the installation process.

If you encounter any issues, you can also use the terminal within the installer to manually configure the WiFi connection using `nmcli` (NetworkManager command-line interface) commands:

1. **Access the Terminal**:
   - Press `Ctrl` + `Alt` + `F2` to switch to a terminal.

2. **Use nmcli to Connect to WiFi**:
   - List available WiFi networks:
     ```bash
     nmcli dev wifi list
     ```
   - Connect to your WiFi network:
     ```bash
     nmcli dev wifi connect "SSID_NAME" password "YOUR_WIFI_PASSWORD"
     ```
   - Replace `"SSID_NAME"` with your WiFi network name and `"YOUR_WIFI_PASSWORD"` with your WiFi password.

3. **Switch Back to Installer**:
   - Press `Ctrl` + `Alt` + `F1` to return to the installer interface.

These steps should help you configure your WiFi connection during the Ubuntu Server installation.

## Password Reset

If you need to reset the password for a user, follow these steps:

### From Normal Boot

1. **Open Terminal**:
   - Log in with a user that has sudo privileges and open a terminal.
2. **Reset Password**:
   ```bash
   sudo passwd harsh_server
   ```
   - Enter the new password when prompted.

### From Recovery Mode

1. **Reboot and Enter Recovery Mode**:
   - Hold `Shift` during boot to access the GRUB menu.
   - Select `Recovery mode` and then `root` to drop to a root shell prompt.
2. **Remount Filesystem as Read/Write**:
   ```bash
   mount -o remount,rw /
   ```
3. **Reset Password**:
   ```bash
   passwd harsh_server
   ```
4. **Reboot the System**:
   ```bash
   reboot
   ```

## Listing Users

To list all users on the system:
```bash
cut -d: -f1 /etc/passwd
```

## SSH Connection

To connect to your server via SSH:
1. **Ensure SSH is Installed**:
   ```bash
   sudo apt update
   sudo apt install openssh-server
   ```
2. **Connect via SSH**:
   ```bash
   ssh harsh_server@192.168.1.101
   ```
   Replace `192.168.1.101` with your server's IP address.

## GRUB Configuration

1. **Edit GRUB Configuration**:
   - Open `/etc/default/grub`:
     ```bash
     sudo nano /etc/default/grub
     ```
   - Modify the following lines:
     ```plaintext
     GRUB_TIMEOUT_STYLE=menu
     GRUB_TIMEOUT=5
     ```
   - Save and exit the file.
2. **Update GRUB**:
   ```bash
   sudo update-grub
   ```
