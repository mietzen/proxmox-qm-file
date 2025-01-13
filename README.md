# qm-file

`qm-file` is a Python script designed to transfer files to and from virtual machines (VMs) managed by Proxmox VE. It uses the `qm guest exec` command to execute file operations inside the VM and supports chunked file transfers for large files.

## Caveats:

- **File transfer is really slow!** Only around **90-350 KB/s** depending on the server load.
- **Only Linux and FreeBSD VMs** are supported.

## Syntax
```
$ ./qm-file -h
usage: qm-file [-h] [-v] [--no-progress] [--no-checks] [--no-verify] vmid {put,fetch} file_in file_out

Put / Fetch file in chunks from / to a VM.

positional arguments:
  vmid           VM ID
  {put,fetch}    Transfer mode
  file_in        Path of input file
  file_out       Path of output file

options:
  -h, --help     show this help message and exit
  -v, --verbose  Increase verbosity (e.g., -v, -vv, -vvv)
  --no-progress  Don't show progress
  --no-checks    Don't run checks
  --no-verify    Don't verify files
```

## Install

```bash
sudo curl -o /usr/sbin/qm-file https://raw.githubusercontent.com/mietzen/proxmox-qm-file/refs/heads/main/qm-file
sudo chmod +x /usr/sbin/qm-file
```

## Uninstall

```
sudo rm /usr/sbin/qm-file
```

## Examples

### Uploading a File to a VM
```bash
$ ./qm-file -vv 100 put ./file.bin /tmp/file.bin
2025-01-13 15:16:01 [INFO] Guest agent is installed and reachable.
2025-01-13 15:16:02 [INFO] OS check passed: name='debian gnu/linux', kernel-version='#1 smp preempt_dynamic debian 6.1.119-1 (2024-11-22)'.
2025-01-13 15:16:03 [INFO] Command 'cat' is available.
2025-01-13 15:16:04 [INFO] Command 'dd' is available.
2025-01-13 15:16:05 [INFO] Command 'stat' is available.
2025-01-13 15:16:06 [INFO] Command 'base64' is available.
2025-01-13 15:16:07 [INFO] Command 'sha256sum' is available.
2025-01-13 15:16:07 [INFO] Starting operation: put
2025-01-13 15:16:07 [INFO] File size: 5000000 bytes. Number of chunks: 5.
2025-01-13 15:16:07 [WARNING] File will be transferred in 5 chunks due to its size.
2025-01-13 15:16:07 [INFO] Transferring chunk of size 1048575 bytes (1/5).
2025-01-13 15:16:10 [INFO] Transferring chunk of size 1048575 bytes (2/5).
2025-01-13 15:16:13 [INFO] Transferring chunk of size 1048575 bytes (3/5).
2025-01-13 15:16:16 [INFO] Transferring chunk of size 1048575 bytes (4/5).
2025-01-13 15:16:19 [INFO] Transferring chunk of size 805700 bytes (5/5).
2025-01-13 15:16:21 [INFO] File: ./bin.file (5000000 bytes). Transfer completed, in 14.6 s (334.3 KB/s)
2025-01-13 15:16:22 [INFO] Got sha256 checksum from remote file: e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d
2025-01-13 15:16:22 [INFO] Got sha256 checksum from local file:  e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d
```

### Downloading a File from a VM
```bash
$ ./qm-file -vv 100 fetch /tmp/file.bin file.bin
2025-01-13 15:17:30 [INFO] Guest agent is installed and reachable.
2025-01-13 15:17:31 [INFO] OS check passed: name='debian gnu/linux', kernel-version='#1 smp preempt_dynamic debian 6.1.119-1 (2024-11-22)'.
2025-01-13 15:17:32 [INFO] Command 'cat' is available.
2025-01-13 15:17:33 [INFO] Command 'dd' is available.
2025-01-13 15:17:34 [INFO] Command 'stat' is available.
2025-01-13 15:17:35 [INFO] Command 'base64' is available.
2025-01-13 15:17:36 [INFO] Command 'sha256sum' is available.
2025-01-13 15:17:36 [INFO] Starting operation: fetch
2025-01-13 15:17:36 [INFO] File size: 5000000 bytes. Number of chunks: 3.
2025-01-13 15:17:36 [WARNING] File will be fetched in 3 chunks due to its size.
2025-01-13 15:17:36 [INFO] Transferring chunk of size 2097152 bytes (1/3).
2025-01-13 15:17:55 [INFO] Transferring chunk of size 2097152 bytes (2/3).
2025-01-13 15:18:16 [INFO] Transferring chunk of size 805696 bytes (3/3).
2025-01-13 15:18:19 [INFO] File: /tmp/file.bin (5000000 bytes). Transfer completed, in 42.1 s (115.8 KB/s)
2025-01-13 15:18:20 [INFO] Got sha256 checksum from remote file: e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d
2025-01-13 15:18:20 [INFO] Got sha256 checksum from local file:  e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d
```
