```markdown
# Dual Boot GRUB Configuration

This guide documents the steps taken to configure the GRUB bootloader for a dual-boot system with Windows 11 Pro and Ubuntu 22.04. The primary goals were to change the timeout for the OS selection menu and set Windows as the default operating system.

## System Setup

- **Operating Systems**: Windows 11 Pro, Ubuntu 22.04
- **Bootloader**: GRUB
- **Disk Configuration**: Windows on `/dev/nvme0n1p1`

## Objective

1. Change the timeout for the GRUB OS selection menu to 5 seconds.
2. Set Windows as the default OS in the GRUB menu.

## Steps Taken

### Step 1: Boot into Ubuntu

1. Start the computer and boot into Ubuntu.

### Step 2: Open Terminal

1. Press `Ctrl + Alt + T` to open the terminal.

### Step 3: Edit GRUB Configuration

1. Open the GRUB configuration file in a text editor with superuser privileges:
   ```sh
   sudo nano /etc/default/grub
   ```

2. Modify the following lines to set the timeout and default OS:
   - Set the `GRUB_DEFAULT` to Windows by specifying its menu entry.
   - Set the `GRUB_TIMEOUT` to 5 seconds.
   - Ensure the `GRUB_TIMEOUT_STYLE` is set to `menu` to display the menu.

   ```sh
   # If you change this file, run 'update-grub' afterwards to update
   # /boot/grub/grub.cfg.
   # For full documentation of the options in this file, see:
   #   info -f grub -n 'Simple configuration'

   GRUB_DEFAULT="Windows Boot Manager (on /dev/nvme0n1p1)"
   GRUB_TIMEOUT_STYLE=menu
   GRUB_TIMEOUT=5
   # GRUB_DEFAULT=0
   # GRUB_TIMEOUT_STYLE=hidden
   # GRUB_TIMEOUT=10
   GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
   GRUB_CMDLINE_LINUX=""

   # Uncomment to enable BadRAM filtering, modify to suit your needs
   # This works with Linux (no patch required) and with any kernel that obtains
   # the memory map information from GRUB (GNU Mach, kernel of FreeBSD ...)
   #GRUB_BADRAM="0x01234567,0xfefefefe,0x89abcdef,0xefefefef"
   ```

3. Save the file and exit the editor:
   - Press `Ctrl + X`, then `Y` to confirm, and `Enter` to save.

### Step 4: Update GRUB

1. Run the following command to update the GRUB configuration:
   ```sh
   sudo update-grub
   ```

### Step 5: Verify GRUB Configuration

1. Open the generated GRUB configuration file to ensure changes are applied:
   ```sh
   sudo nano /boot/grub/grub.cfg
   ```

2. Look for the lines similar to:
   ```sh
   set default="Windows Boot Manager (on /dev/nvme0n1p1)"
   set timeout=5
   ```

3. Save and close the file if changes are correct.

### Step 6: Check for Custom Scripts

1. List the files in the `/etc/grub.d/` directory to check for custom scripts:
   ```sh
   ls /etc/grub.d/
   ```

2. Verify that there are no custom scripts that might interfere with the GRUB configuration.

### Step 7: Reinstall GRUB (if necessary)

1. If the previous steps did not work, reinstall GRUB to ensure proper configuration:
   ```sh
   sudo grub-install /dev/nvme0n1
   sudo update-grub
   ```

### Step 8: Reboot

1. Restart the computer to see if the changes take effect:
   ```sh
   sudo reboot
   ```

## Conclusion

By following these detailed steps, we successfully configured the GRUB bootloader to set Windows as the default OS and adjusted the timeout for the OS selection menu. These steps can be useful for future reference or similar configurations on other dual-boot systems.
```
