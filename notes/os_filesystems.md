## Reboot vs Stop
**1. In AWS EC2 world**
For both reboot + instance stop/start, private IP address of the instance doesn't change until the instance is terminated.
- Reboot = OS reboot, the underlying host doesn't change. This means that the attached instance store will still remain attached.
- Instance stop->start however signals that the VM gives up the slot on the underlying host and so the attached instance store may be lost when it's started back on another host.

**2. In Generic Linux world**
**2.1. Forceful Shutdown**
If the system is shutdown in a forceful way (e.g. by pressing a hardware reset button or by removing the power cord), everything that is stored only in RAM will be lost. This means if data is buffered in the filesystem cache and not fsynced to disk yet, those will be lost.
A boot-time filesystem check will detect that filesystems were not properly mounted: journalling filesystems will usually execute a journal recovery automatically to keep the filesystem metadata internally consistent, but unless the data is also journalled, you may find that some data did not actually reach the disk (this may appear as strings of repeated \000 in log files, as the last block allocated but not written has only zero bytes in it). Databases may also need to execute some sort of consistency recovery actions after a forceful shutdown.

**2.2. Normal, controlled Shutdown/Reboot**
- `SIGHUP` signal sent to all processes belonging to users' login sessions, allowing them to perform cleanup (e.g. saving backup of unsaved work) before exiting. If there are user processes / system services that are not shutting down after timeout, a `SIGTERM` signal will be sent before a `SIGKILL` signal st processes will have the chance to either complete/rollback actions. Ultimately, processes must be terminated st all files can be closed for unmounting the file systems cleanly.
- Shutting down system services in an ordered manner, st services that are dependent on other services are shut down before they are shutdown. (e.g. `opensearch` service -> ... -> `networkd` service).
- After number of processes left running is reduced to the minimum req'd, unmounting any network-based filesystems in a controlled manner, ensuring that any cached write operations are fsynced before unmounting. Then shutting down services related to accessing network file systems.
- Completing any cached write operations to local disks, then unmounting those disks (**except the root file system** which is usually just switched to read-only mode instead).
- Kernel is told to send the hardware signal to power off / reset the system.


## What is in Root disk (AWS Linux)
There are 2 partitions in the root volume -- BIOS boot partition; rest of the root volume (`/`)
![lsblk_root_vol](https://miro.medium.com/v2/resize:fit:640/format:webp/1*qawkLiF99OBSWJeU8XTpXg.png)

**1. Master Boot Record**
The Master Boot Record (MBR) is the first 512 bytes of a storage device. It contains an operating system bootloader and the storage device's partition table. It plays an important role in the boot process under BIOS systems

**2. Directories under the root disk**
1. root dir: `/`
2. boot dir for initramfs images + boot loader config file + boot loader stages `/boot`
3. other directories e.g. `/var`, `/tmp`, `/etc`, ...

**2.1. Root Directory `/`**
The root directory is the top of the hierarchy, the point where the primary filesystem is mounted and from which all other filesystems stem. All files and directories appear under the root directory /, even if they are stored on different physical devices. The contents of the root filesystem must be adequate to boot, restore, recover, and/or repair the system.

**2.2 Boot Directory `/boot`**
`boot` directory contains `vmlinuz`, `initramfs` images + boot loader config file + boot loader stages. It also stores data used before the kernel starts executing user-space programs. Only required during boot + kernel upgrades (when regenerating initramfs), not req'd for normal system operation.

## Linux Boot process
![boot_process](https://www.freecodecamp.org/news/content/images/2020/03/LinuxBootingProcess.jpg)

**Terminology**
**init**
There are 2 different processes assoc with init:
- (`init` on `initramfs`) `initramfs` process mounting the root fs
- (`systemd` - initial process in the Operating system) operating system process starting all other processes executed from the actual root fs
**initrd/initramfs**
`initrd` (initial RAM disk) is an image file containing a root fs image that is loaded by the kernel and mounted from `/dev/ram` as the temporary root file system. Before kernel 2.6.13 mounting this file system requuires a filesystem driver.
For kernels >= 2.6.13 , `initrd` has been replaced by `initramfs` (initial RAM fs) that doesn't require a fs driver and is mounted into the fs as `/boot/initrd`.

**Stages**
1. Hardware setup + Boot Loader Phase
2. Kernel Phase
3. `init` on `initramfs` phase
4. `systemd` phase

**1. BIOS > read Master Boot Record > execute BootLoader (GRUB)**
BIOS (Basic Input/Output System) loads and executes the (MBR) Master Boot Record boot loader that is located in the first 512B of the root disk sector `/dev/sda`.
- When the host is first powered on, the BIOS performs some integrity checks on the HDD/SSD. It does so by checking for the boot signature at the end of the first sector (storing MBR)
- BIOS searches, loads and executes the boot loader program located in the Master Boot Record (MBR). 
- Boot loader program is loaded into memory and the BIOS gives control of the system to it.

![mbr_0](https://miro.medium.com/v2/resize:fit:640/format:webp/1*Sn1p3bd8qNy3ecaABuRwDQ.png)
![mbr_1](https://miro.medium.com/v2/resize:fit:640/format:webp/1*32O0O7c_lNzYYagdaUrJCQ.png)
**MBR contains:**
— The 𝒇𝒊𝒓𝒔𝒕 446 𝒃𝒚𝒕𝒆𝒔 contains the code for the 𝒃𝒐𝒐𝒕𝒍𝒐𝒂𝒅𝒆𝒓 (typically 𝑮𝑹𝑼𝑩 in Linux distros)
— The next 64 𝒃𝒚𝒕𝒆𝒔 contains the 𝒑𝒂𝒓𝒕𝒊𝒕𝒊𝒐𝒏 𝒕𝒂𝒃𝒍𝒆 for that disk
— The last 2 𝒃𝒚𝒕𝒆𝒔 contains the 𝒃𝒐𝒐𝒕 𝒔𝒊𝒈𝒏𝒂𝒕𝒖𝒓𝒆 which is used to identify the storage device (The value is 0x55AA).

**1.1. Executing Stage 1 of GRUB**
- As GRUB is too large to fit within the first 446B of the disk, MBR config uses a 3-stage bootloader process. Stage 1 of the bootloader process is used to load stage 1.5 of the bootloader process into RAM.
![grub_3stage_process](https://miro.medium.com/v2/resize:fit:640/format:webp/0*Z69HhvsRaItaNAlo.png)

**1.2. Executing Stage 1.5 of GRUB**
- Stage 1.5 is stored in the empty raw sectors on the disk between the MBR (first 512B) and the first partition. (Hence the BIOS Boot Partition needs to be large enough e.g. 1MB to store the full GRUB)
- If the GUID Partition Table (GPT) standard is used, GPT headers will occupy this space instead and stage 1.5 of GRUB will be stored in a dedicated small partition. (Most Linux Distros used GPT)

**1.2.1. GPT vs MBR**
The Globally Unique Identifiers Partition Table is the modern replacement for the antique MS-DOS Master Boot Record (MBR). The MBR was born in the early 1980s for IBM PCs, way back in the thrilling days of ten-megabyte hard disks. The MBR must live on the first 512 bytes of your storage device, and it holds the bootloader and partition table. The bootloader occupies 446 bytes, the partition table uses 64 bytes, and the remaining two bytes store the boot signature. The MBR is tiny and inflexible.

GPT has several advantages over the MBR: 
- 64-bit disk pointers allows 264 total sectors, so a hard disk with 512-byte blocks can be as large as 8 zebibytes. With 4096-byte sectors your maximum disk size is really really large
- Unique IDs for disks and partitions.
- GPT has fault-tolerance by keeping copies of the partition table in the first and last sector on the disk

**1.2.2.1 GPT GUIDs**
GPT GUIDs are different from Linux UUIDs even though they both give block devices unique names. You can use both UUIDs / GUIDs in `/etc/fstab`.

**Linux UUIDs**
- Linux UUIDs are a function of filesystems and a new UUID is created when a new filesystem is created. This also means that if a disk partition is reformatted to use a new filesystem type (e.g. xfs -> ext4), the linux UUID will change but the GUID will remain the same since the disk partition is still the same.
`blkid` shows Linux UUIDs.
```sh
blkid 
# /dev/sda1: LABEL="storage" UUID="60e97193-e9b2-495f-8db1
#   -651f3a87d455" TYPE="ext4" 
# /dev/sda2: LABEL="oldhome" UUID="e6494a9b-5fb6-4c35-ad4c-
#    86e223040a70" TYPE="ext4" 

cat /etc/fstab
# /etc/fstab
# Note that here we use UUID=
# UUID=60e97193-e9b2-495f-8db1-651f3a87d455 /home/carla/storage ext4 user,defaults 0 0
```

**GPT GUIDs**
- Use `gdisk` to view disk partition UUIDs. These partition UUIDs are assigned when a new disk partition is created.
```sh
cat /etc/fstab
# /etc/fstab
# Note that here we use PARTUUID= to identify UUID of partition
# PARTUUID=8C208C30-4E8F-4096-ACF9-858959BABBAA /data ext4 user,defaults 0 0
```

**1.3. GRUB Stage 2**
- After GRUB stage 1.5 is loaded into memory, the host has the necessary filesystem drivers to locate and load stage 2 from `/boot` directory into memory.
- Once GRUB stage 2 is loaded, a GRUB menu will be displayed to allow users to pick whichever kernel image (if multiple are loaded, or use the default kernel image).

The GRUB config file is located at `/boot/grub/grub.conf` / `/etc/grub.conf`.
e.g. 
```sh
#boot=/dev/sda
default=0
timeout=5
splashimage=(hd0,0)/boot/grub/splash.xpm.gz
hiddenmenu
title CentOS (2.6.18-194.el5PAE)
      root (hd0,0)
      kernel /boot/vmlinuz-2.6.18-194.el5PAE ro root=LABEL=/ <------- kernel image
      initrd /boot/initrd-2.6.18-194.el5PAE.img              <------- initrd image
```

**2. Kernel Initialization**
- GRUB boot loader loads the Kernel image into memory from `/boot/vmlinuz-<version>.` on disk. The kernel image path is specified in the GRUB config file.
- Req'd kernel modules are stred in `/lib/modules/` directory. However, for the kernel to access this directory and load the necessary kernel modules, it needs to first mount the root file system. To get around this, we use `initramfs` which is a tmp file system containing all the essential drivers + modules for the kernel to mount the actual file system.

![ls_boot_dir](https://miro.medium.com/v2/resize:fit:640/format:webp/1*wt4Mija5AKl3GSgz1hva7A.png)

**2.1 Loading initramfs**
- GRUB boot loader loads the initial RAM filesystem (initramfs) + kernel image into memory. Then GRUB passes control to the kernel.
- Kernel initializes the hardware components and configures memory.
- Kernel extracts the `initramfs` into a tmp filesystem (`tmpfs`) which allows it to access the `/lib/modules/` dir and load the req'd kernel modules to boot the system.

We can verify the kernel extracting `initramfs` in `dmesg`
![initramfs_dmesg](https://miro.medium.com/v2/resize:fit:640/format:webp/1*Iy5fL8hLoeL45BtOSidoLA.png)

**3. Transition from Kernel to User Space**
![init_script](https://miro.medium.com/v2/resize:fit:640/format:webp/1*PhnyOXGCyr0vQQgJa62MfQ.png)
- Kernel executes the init / systemd script (depending on init system used) from `initramfs`. This init script (1) loads the req'd drivers for accessing the root filesystem; (2) mounts the real root file system (e.g. from `/dev/sda1`)
- Once the real file system is mounted, the init script switches the root filesystem from `initramfs` to the real root filesystem by:
    - deleting everything out of `rootfs` to free the space in `tmpfs` (`find -xdev / -exec rm '{}' ';'`)
    - then overmounting `rootfs` with the new root filesystem (`cd /newmount; mount -- mv . /; chroot .`)
    - then attaching stdin/stdout/stderr to the new `/dev/console` and exec the new init process.
- After switching to the real root filesystem, the `init` script executes the `init process` (located at `/sbin/init`). This process is the first user-space process with PID 1. It is responsible for starting all other user-space processes.
![init_script](https://miro.medium.com/v2/resize:fit:640/format:webp/1*zEU5jirRiR6nmaWA7lkKFg.png)

**4. System Initialization**
- Init process initializes the system by running its respective init script (e.g. for systemd, this is the `basic.target` script)
- The system's hostname is set based on the config in `/etc/hostname`.
- `initramfs` is unmounted and cleaned up after the real root filesystem has been successfully mounted and system has `chroot` to using it.
- Kernel parameters are set based on `/etc/sysctl.conf` and any files in `/etc/sysctl.d/`. These parameters control kernel behavior e.g. networking (MTU, dns cache ttl), security, performance.
- Device filesystem `devfs` is started to manage device nodes in `/dev`. This allows the system to dynamically create and manage device nodes for hardware components.
    ```sh
    mount -t devtmpfs devtmpfs /dev
    ```
    ![devtmpfs](https://miro.medium.com/v2/resize:fit:640/format:webp/1*dbUDBc376an81d2DzTscDQ.png)
- Process filesystem and sys filesystem are mounted to provide access to process, kernel information respectively.
    ```sh
    mount -t proc proc /proc
    mount -t sysfs sysfs /sys
    ```
    ![proc_sys_fs](https://miro.medium.com/v2/resize:fit:640/format:webp/1*WVsPLlZHcxj2G31SM96wMQ.png)
- (Optional) Enabling RAID/LVM. RAID arrays and LVM volumes are activated if enabled. This step ensures that all storage devices are properly configured and available.
    ```sh
    mdadm --assemble --scan
    vgchange -ay
    ```
- `/etc/fstab` file is processed to mount file systems and run filesystem consistency checks (`fsck`). This ensures that all filesystems are mounted and checked for consistency.
    ```sh
    mount -a
    ```
- Kernel Ring Buffer contents are dumped to `/var/log/dmesg` for logging purposes for diagnosing boot issues and understanding kernel messages.
    ```sh
    dmesg > /var/log/dmesg
    ```
- Additional kernel modules specified in configuration files (e.g. `/etc/modules`, `/etc/modprobe.d`) are loaded. This ensures that all req'd hardware drivers are available.
    ```sh
    modprobe <module_name>
    ```
- Systemd loads default systemd target from `/etc/systemd/system/default.target` and starts the services and dependencies defined in the systemd target.
    ![systemd_default_target](https://miro.medium.com/v2/resize:fit:640/format:webp/1*2oKS__CS2njPTvAhWenZgg.png)
- `/etc/rc.d/rc.local` script is run to execute any custom commands at the end of the boot process.
    ![rc_local_script](https://miro.medium.com/v2/resize:fit:640/format:webp/1*0Jxk5vYym3DP4cgVRPph3Q.png)


## Cloudinit
**When is userdata script run for AWS ec2:**
The script is run by `/etc/init.d/cloud-init-user-scripts` during the first boot cycle. This occurs late in the boot process (after the initial configuration actions are performed).
![cloudinit0](https://leftasexercise.com/wp-content/uploads/2020/04/cloudinitoverview.png)
https://leftasexercise.com/2020/04/12/understanding-cloud-init/


### How to fix corrupted root disk
If `dmesg` shows that filesystem mount in `/etc/fstab` is corrupted during cloudinit, we can stop target instance A, unmount root volume, remount it onto rescue instance B as another device (e.g. `/dev/sdb`) under directory `/corruptedroot`. Since corrupted root volume device is already formatted to use some file system, we don't have to do that again. We can just comment out the corrupted fs mount in `/etc/fstab` and then detach root volume and remount back onto A.

### How to repartition root disk
1. Detach root disk from instance A, remount root disk onto instance B as another device (e.g. `/dev/nvme2n1`).
2. List partitions on devices by running `parted -l`.
We see that `/dev/nvme0n1`, `/dev/nvme1n1` both have partitions. We want to split `/dev/nvme2n1` to have the following partitions -- `BIOS Boot Partition` (1M -> 2M), `/`, `/home`, `/var`, `/tmp`.
![parted_ls_partitions](https://miro.medium.com/v2/resize:fit:640/format:webp/1*c_boQUdp65tal-rntkbdUA.png)
3. Create a BIOS Boot Partition (GPT record) by running `parted /dev/nvme2n1`
```sh
# parted /dev/nvme2n1 

(parted) mklabel gpt
(parted) mkpart "BIOS Boot Partition" 1MB 2MB
(parted) set 1 bios_grub on
```
![create_bios_boot_partition](https://miro.medium.com/v2/resize:fit:640/format:webp/1*Uu888utukznQHqUz3PHzzA.png)
4. Create the other partitions.
```sh
# (parted) mkpart part-type name fs-type start end
#  Replace start and end with the sizes that determine the starting and ending points of the partition, counting from the beginning of the disk. You can use size suffixes, such as 512MiB, 20GiB, or 1.5TiB. The default size is in megabytes. 
(parted) mkpart root xfs 2MB 30%
(parted) mkpart home xfs 30% 50%
(parted) mkpart var xfs 50% 80%
(parted) mkpart tmp xfs 80% 100% 
```
![lsblk](https://miro.medium.com/v2/resize:fit:640/format:webp/1*zbx3w0lOjLdWROac6WVlmQ.png)
5. Format the new partitions to use `xfs` filesystem
```sh
mkfs.xfs /dev/nvme2n1p2
mkfs.xfs /dev/nvme2n1p3
mkfs.xfs /dev/nvme2n1p4
mkfs.xfs /dev/nvme2n1p5
lsblk -f
```
![lsblk_filesystem](https://miro.medium.com/v2/resize:fit:640/format:webp/1*AmSGw9zhG8Rh0xenh3jZVg.png)
6. Mount the partitions onto the filesystem paths on rescue instance B.
```sh
# create dir for source vol
mkdir /mnt/source_vol
# create dirs for target vol (this is where we're be cloning root vol from source_vol to)
mkdir /mnt/target_vol/
mkdir /mnt/target_vol/root 
mkdir /mnt/target_vol/home 
mkdir /mnt/target_vol/var
mkdir /mnt/target_vol/tmp

# mount partitions onto dirs
# mount source vol onto /dev/nvme1n1p2
mount -o nouuid /dev/nvme1n1p2 /mnt/source_vol/
mount /dev/nvme2n1p2 /mnt/target_vol/root/
mount /dev/nvme2n1p3 /mnt/target_vol/home/
mount /dev/nvme2n1p4 /mnt/target_vol/var/
mount /dev/nvme2n1p5 /mnt/target_vol/tmp/

# sync source vol content to the target vol partitions
rsync -av /mnt/source_vol/home/ /mnt/target_vol/home/
rsync -av /mnt/source_vol/var/ /mnt/target_vol/var/
rsync -av /mnt/source_vol/tmp/ /mnt/target_vol/tmp/
# rsync remaining content in `/` root dir (this includes the `/boot` directory)
rsync -av --exclude=home --exclude=var --exclude=tmp /mnt/source_vol/ /mnt/target_vol/root/

# verifying target root directory
ls -la /mnt/target_vol/root/
```
![target_vol_root](https://miro.medium.com/v2/resize:fit:640/format:webp/1*y-TOO5TEOJOT64b-9RxDlQ.png)
7. Install GRUB on the new volume
```sh
# chroot to the target volume so that `/mnt/target_vol/root` effectively becomes 
for m in dev proc run sys; do mount -o bind {,/mnt/target_vol/root}/$m; done
chroot /mnt/target_vol/root

# move the old GRUB config file
mv /boot/grub2/grub.cfg /boot/grub2/grub.cfg.org

# install the GRUB boot loader in the target volume
grub2-install /dev/nvme2n1

# regenerate GRUB config file
grub2-mkconfig -o /boot/grub2/grub.cfg
```
8. Edit `/etc/fstab` file and set new partitions
```sh
# backup old /etc/fstab file
cp /etc/fstab /etc/fstab.org

# add new partitions to /etc/fstab file based on UUIDs from `lsblk -f` output
lsblk -f
# NAME        FSTYPE LABEL UUID                                 MOUNTPOINT
# nvme1n1                                                       
# ├─nvme1n1p1                                                   
# └─nvme1n1p2 xfs    root  eaa1f38e-de0f-4ed5-a5b5-2fa9db43bb38 
# nvme0n1                                                       
# ├─nvme0n1p1                                                   
# └─nvme0n1p2 xfs    root  eaa1f38e-de0f-4ed5-a5b5-2fa9db43bb38 
# nvme2n1                                                       
# ├─nvme2n1p1                                                   
# ├─nvme2n1p2 xfs          ddc82b07-5b7e-484a-8729-64972c5ca3f8 /
# ├─nvme2n1p3 xfs          6f0d0200-b0dd-4d71-94d5-bdcd59b8c2a5 /home
# ├─nvme2n1p4 xfs          3f79719b-5aa9-4610-9249-91ccf9a2e9cf /var
# └─nvme2n1p5 xfs          69d358b3-9dfa-4dcf-8081-9bc919d50c8e /tmp
cat /etc/fstab
# UUID=ddc82b07-5b7e-484a-8729-64972c5ca3f8  /      xfs  defaults    0  0
# UUID=6f0d0200-b0dd-4d71-94d5-bdcd59b8c2a5  /home  xfs  defaults    0  0
# UUID=3f79719b-5aa9-4610-9249-91ccf9a2e9cf  /var   xfs  defaults    0  0
# UUID=69d358b3-9dfa-4dcf-8081-9bc919d50c8e  /tmp   xfs  defaults    0  0   
```
9. Unmount the volume for device `/dev/nvme2n1` and attach it back onto instance A.
```sh
umount /mnt/target_vol/root/{dev,proc,run,sys,home,var,tmp,}
```

## A/B root disk partition upgrades
but if we swap root disk, hostname could change since hostname is defined in `/etc/hostname` unless we resync data under `/` root partition and only swap out the BIOS Boot Partition.

TODO: how does AWS ec2 root volume replacement work? Does it implement A/B root disk partition swap

## Device < Partition < (Optional) LVM < Filesystem
TODO

## Filesystem Journaling
Metadata vs Data journaling (eg. on ext4)
TODO

## Filesystem buffering + Writeback cache
TODO

## Raid0 vs LVM Striping
TODO

## Disk Read/Write
![fs_read](https://www.scylladb.com/wp-content/uploads/Chart_1@1x.svg)
TODO

## MMAP
TODO
