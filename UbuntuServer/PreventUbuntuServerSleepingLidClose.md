# Prevent Ubuntu Server from Sleeping on Lid Close

## Overview

This README provides instructions to configure your Ubuntu Server to remain awake when the laptop lid is closed.

## Steps

1. **Edit `logind.conf` File:**
   - Open a terminal on your Ubuntu Server.

   - Edit the `logind.conf` file using a text editor:
     ```
     sudo nano /etc/systemd/logind.conf
     ```

   - Find the line `HandleLidSwitch=suspend`.

   - Uncomment the line (remove the `#` at the beginning if it exists) and change `suspend` to `ignore`:
     ```
     HandleLidSwitch=ignore
     ```

   - Save the file (`Ctrl + O`, `Enter`) and exit (`Ctrl + X`).

2. **Restart systemd-logind:**
   - Apply the new configuration by restarting the `systemd-logind` service:
     ```
     sudo systemctl restart systemd-logind
     ```

## Verification

To verify that the configuration is successful, close the laptop lid and ensure that the Ubuntu Server remains active.

## Troubleshooting

If the Ubuntu Server still sleeps when the lid is closed, double-check the changes made to `logind.conf` and ensure that `HandleLidSwitch=ignore` is correctly set.
