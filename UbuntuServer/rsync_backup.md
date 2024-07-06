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
