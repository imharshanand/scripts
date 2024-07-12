### Backup Documentation

#### Overview
You created a complete backup of your Ubuntu server using `rsync` and stored it on a separate partition mounted at `/mnt/live_storage`.

#### Prerequisites
- Ensure `rsync` is installed:
  ```bash
  sudo apt install rsync
  ```
- Ensure the backup destination is properly mounted. In this case, `/mnt/live_storage` is the backup destination.

#### Backup Command
You used the following `rsync` command to back up your entire system:

```bash
sudo rsync -av --delete \
  --exclude={"/mnt","/proc","/sys","/dev","/run","/media","/lost+found"} \
  / /mnt/live_storage/backup
```

##### Command Breakdown
- `sudo`: Run as superuser to ensure all files are accessible.
- `rsync`: The tool used for copying files.
- `-a`: Archive mode, which preserves permissions, symbolic links, etc.
- `-v`: Verbose mode, which provides detailed output.
- `--delete`: Deletes files in the destination that are not in the source to keep the backup in sync.
- `--exclude`: Excludes specific directories that shouldn’t be backed up.
- `/`: The root directory of your server (source).
- `/mnt/live_storage/backup`: The backup destination.

### Restore Documentation

#### Overview
To restore your system from the backup created, you will use the `rsync` command to copy files back from the backup directory to the root directory.

#### Prerequisites
- Boot from a live CD/USB if the system is not bootable.
- Mount the root filesystem and the backup location.

#### Steps to Restore

1. **Boot from a Live CD/USB**: If your system is not bootable, boot from a live CD/USB.
2. **Open Terminal**: Open a terminal from the live session.
3. **Mount the Root Filesystem**: Mount the root filesystem of your server. Replace `/dev/sda7` with your root partition.
   ```bash
   sudo mount /dev/sda7 /mnt
   ```
4. **Mount the Backup Storage**: Mount the backup storage if it’s not automatically mounted. Replace `/dev/sdb3` with your backup partition.
   ```bash
   sudo mount /dev/sdb3 /mnt/live_storage
   ```
5. **Run the rsync Command**: Use `rsync` to restore files from the backup directory to the root filesystem.
   ```bash
   sudo rsync -av --delete /mnt/live_storage/backup/ /mnt/
   ```
6. **Chroot into the Mounted Filesystem**: To reinstall the bootloader or make any necessary adjustments, chroot into the mounted filesystem.
   ```bash
   sudo chroot /mnt
   ```
7. **Update the Bootloader** (if needed): If you need to reinstall the bootloader, you can do so from the chroot environment. For example, to reinstall GRUB:
   ```bash
   grub-install /dev/sda
   update-grub
   ```
8. **Exit chroot and Unmount Filesystems**:
   ```bash
   exit
   sudo umount /mnt
   sudo umount /mnt/live_storage
   ```
9. **Reboot**: Reboot your system.
   ```bash
   sudo reboot
   ```


### Steps to Delete the Old Backup

1. **Navigate to the Backup Directory**:
   ```bash
   cd /mnt/live_storage/
   ```

2. **List the Contents**:
   ```bash
   ls
   ```
   This command will list all the directories in `/mnt/live_storage`, including the old backup directory `backup2`.

3. **Remove the Old `backup2` Directory**:
   Use `sudo` to ensure you have the necessary permissions to delete the write-protected directory.
   ```bash
   sudo rm -r /mnt/live_storage/backup2
   ```
   - `sudo`: Run as superuser to ensure all files are accessible.
   - `rm -r`: Remove the directory and its contents recursively.

### Steps to Create a New Backup with Exclusion

1. **Ensure `rsync` is Installed**:
   Verify that `rsync` is installed on your system.
   ```bash
   sudo apt install rsync
   ```

2. **Create a New Backup Directory**:
   Create a new directory within your backup storage to store the new backup. This ensures that the old backup is not overwritten.
   ```bash
   sudo mkdir /mnt/live_storage/backup2
   ```

3. **Run the `rsync` Command with Exclusion**:
   Use the following `rsync` command to create the new backup, excluding the specified directory.
   ```bash
   sudo rsync -av --delete \
     --exclude={"/mnt","/proc","/sys","/dev","/run","/media","/lost+found","/home/harsh_server/Downloads/SOLID_STATE_DRIVE/TORRENT"} \
     / /mnt/live_storage/backup2
   ```
   #### Command Breakdown:
   - `sudo`: Run as superuser to ensure all files are accessible.
   - `rsync`: The tool used for copying files.
   - `-a`: Archive mode, which preserves permissions, symbolic links, etc.
   - `-v`: Verbose mode, which provides detailed output.
   - `--delete`: Deletes files in the destination that are not in the source to keep the backup in sync.
   - `--exclude`: Excludes specific directories that shouldn’t be backed up. The new addition is `/home/harsh_server/Downloads/SOLID_STATE_DRIVE/TORRENT`.
   - `/`: The root directory of your server (source).
   - `/mnt/live_storage/backup2`: The new backup destination.

### Verifying the New Backup

After the backup process is complete, you can verify the contents and size of the new backup using the following commands:

1. **List the New Backup Directory**:
   ```bash
   ls -lh /mnt/live_storage/backup2
   ```
   - `-l`: Use a long listing format.
   - `-h`: Print sizes in human-readable format (e.g., 1K, 234M, 2G).

2. **Check the Total Size of the New Backup**:
   ```bash
   sudo du -sh /mnt/live_storage/backup2
   ```
   - `-s`: Display only a total for each argument.
   - `-h`: Print sizes in human-readable format.

3. **Get a Detailed Size of Each Subdirectory in the New Backup**:
   ```bash
   sudo du -h --max-depth=1 /mnt/live_storage/backup2
   ```
   - `-h`: Print sizes in human-readable format.
   - `--max-depth=1`: Limit the depth of the directory tree to display.
