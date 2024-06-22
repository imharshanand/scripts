The steps taken to mount an internal Hard Disk for storage purposes on Ubuntu and create a symbolic link for easy access:

---

# Mount Internal Hard Disk for Storage on Ubuntu

This guide explains how to mount an internal Hard Disk for storage purposes on Ubuntu, ensuring it is automatically mounted at boot, and how to create a symbolic link for easy access.

## Conditions

- Ubuntu 20.04/22.04 installed on an SSD
- An additional internal Hard Disk intended for storage
- The internal Hard Disk is formatted with the ext4 journaling file system

## Steps

### 1. Prepare the Hard Disk

Ensure that your internal Hard Disk is formatted with the ext4 journaling file system. This can be done during the Ubuntu installation process or afterward using tools like GParted.

### 2. Mount the Hard Disk

#### During Installation:

1. **Select Installation Type:**
   - Choose “Something else” to manually configure the partitions.

2. **Create a Partition:**
   - Select the internal Hard Disk.
   - Create a new partition with the ext4 journaling file system.
   - Set the mount point to `/mnt/storage`.

3. **Complete the Installation:**
   - Proceed with the installation and finish setting up Ubuntu.

#### Post Installation:

If you need to mount the drive post-installation:

1. **Open Terminal:**
   ```bash
   sudo blkid
   ```

2. **Find the UUID of the Partition:**
   - Identify the UUID of your internal Hard Disk partition.

3. **Edit `/etc/fstab`:**
   - Open the `/etc/fstab` file in a text editor:
     ```bash
     sudo nano /etc/fstab
     ```
   - Add the following line, replacing `your-disk-uuid` with the actual UUID:
     ```bash
     UUID=your-disk-uuid  /mnt/storage  ext4  defaults  0  2
     ```

4. **Save and Exit:**
   - Save the file and exit the editor (`Ctrl + X`, then `Y` to confirm, and `Enter` to save).

5. **Remount All Partitions:**
   ```bash
   sudo mount -a
   ```

6. **Verify the Mount:**
   ```bash
   df -h
   ```

### 3. Create a Symbolic Link for Easy Access

1. **Create a Symbolic Link:**
   ```bash
   ln -s /mnt/storage ~/storage
   ```

2. **Verify the Symbolic Link:**
   ```bash
   ls -l ~
   ```
   - You should see an entry similar to:
     ```bash
     lrwxrwxrwx 1 your_username your_username      12 Jun 22 15:53 storage -> /mnt/storage
     ```

### 4. Create a Desktop Shortcut

1. **Create a Desktop Entry File:**
   - Open a text editor and paste the following content:
     ```ini
     [Desktop Entry]
     Name=Storage
     Comment=Shortcut to /mnt/storage
     Exec=xdg-open /mnt/storage
     Icon=drive-harddisk
     Terminal=false
     Type=Application
     ```
   - Save this file as `Storage.desktop` on your Desktop or in `~/.local/share/applications`.

2. **Make the File Executable:**
   ```bash
   chmod +x ~/Desktop/Storage.desktop
   ```

### Verification

After completing the steps, you should have:

- The internal Hard Disk mounted at `/mnt/storage`.
- A symbolic link in your home directory (`~/storage`) pointing to the mounted drive.
- A desktop shortcut for quick access to the storage drive.

Use the following command to verify the mount:
```bash
df -h
```

You should see an entry for `/mnt/storage`, confirming the setup is correct.

---
