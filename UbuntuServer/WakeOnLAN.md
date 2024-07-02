Configuring Wake-on-LAN on your Ubuntu Server:

# Configuring Wake-on-LAN on Ubuntu Server 24.04

This document provides detailed steps to configure Wake-on-LAN (WoL) on an Ubuntu Server 24.04. It includes the initial configuration, adjustments to make the configuration persistent, and the steps to test WoL from an Android smartphone.

## Step 1: Initial Setup and Verification

### Verify System Information

To understand the system and network setup, run the following commands:

```bash
uname -a
ip link show
ifconfig -a
```

Example output:
```plaintext
Linux harshserver 6.8.0-36-generic #36-Ubuntu SMP PREEMPT_DYNAMIC Mon Jun 10 10:49:14 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eno1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 1000
    link/ether f4:30:b9:98:58:e7 brd ff:ff:ff:ff:ff:ff
    altname enp3s0
3: wlo1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DORMANT group default qlen 1000
    link/ether a0:af:bd:c6:f0:e3 brd ff:ff:ff:ff:ff:ff
    altname wlp5s0

eno1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether f4:30:b9:98:58:e7  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 554  bytes 42671 (42.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 554  bytes 42671 (42.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlo1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.101  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 2401:4900:1cb8:160:a2af:bdff:fec6:f0e3  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::a2af:bdff:fec6:f0e3  prefixlen 64  scopeid 0x20<link>
        ether a0:af:bd:c6:f0:e3  txqueuelen 1000  (Ethernet)
        RX packets 10292  bytes 1822470 (1.8 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 20360  bytes 26171944 (26.1 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### Enable Wake-on-LAN

1. **Verify if Wake-on-LAN is supported:**

```bash
sudo ethtool eno1 | grep Wake-on
```

Example output:
```plaintext
        Supports Wake-on: pumbg
        Wake-on: d
```

2. **Enable Wake-on-LAN:**

```bash
sudo ethtool -s eno1 wol g
```

3. **Verify that Wake-on-LAN is enabled:**

```bash
sudo ethtool eno1 | grep Wake-on
```

Expected output:
```plaintext
        Supports Wake-on: pumbg
        Wake-on: g
```

## Step 2: Make Wake-on-LAN Settings Persistent

### Disable Cloud-Init's Network Configuration

1. **Create a file to disable cloud-init’s network configuration:**

```bash
sudo mkdir -p /etc/cloud/cloud.cfg.d
echo 'network: {config: disabled}' | sudo tee /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
```

### Configure Netplan

1. **Edit the netplan configuration file:** 

```bash
sudo nano /etc/netplan/01-netcfg.yaml
```

2. **Update the configuration to include Wake-on-LAN for `eno1`:**

```yaml
network:
  version: 2
  ethernets:
    eno1:
      dhcp4: true
      wakeonlan: true
  wifis:
    wlo1:
      access-points:
        "kaddu":
          password: "alphabeta69"
      dhcp4: true
```

3. **Apply the netplan configuration:**

```bash
sudo netplan apply
```

### Fix Permissions Warning

1. **If you encounter a permissions warning, set the correct permissions for the netplan configuration file:**

```bash
sudo chmod 600 /etc/netplan/01-netcfg.yaml
```

2. **Apply the netplan configuration again:**

```bash
sudo netplan apply
```

## Step 3: Install and Configure Wake-on-LAN Utility on Android Smartphone

1. **Install a Wake-on-LAN app** from the Google Play Store. Recommended apps:
    - Wake On Lan
    - WolOn
    - Wake On Lan (WOL)

2. **Configure the app with the following details:**
    - **Device Name:** A friendly name for your PC (e.g., "Harsh's Server").
    - **MAC Address:** `f4:30:b9:98:58:e7`
    - **IP Address:** The IP address of your PC (e.g., `192.168.1.101`).
    - **Port:** `9` (default for Wake-on-LAN).

## Step 4: Test Wake-on-LAN

1. **Shutdown your PC.**
2. **Use the Wake-on-LAN app** from your smartphone to send a WoL packet:
    - Open the app.
    - Select the device you configured.
    - Tap the Wake button.

## Additional Tips

- **BIOS/UEFI Settings:** Ensure that Wake-on-LAN is enabled in your BIOS/UEFI settings. This setting is typically found in the Power Management or Advanced settings section.
- **Router Configuration:** If you want to wake your PC over the internet, set up port forwarding on your router to forward the WoL port (usually UDP port 9) to your PC’s IP address.
