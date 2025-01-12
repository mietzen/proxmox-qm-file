# qm-file

`qm-file` is a Python script designed to transfer files to and from virtual machines (VMs) managed by Proxmox VE. It uses the `qm guest exec` command to execute file operations inside the VM and supports chunked file transfers for large files.

## Caveats:

- **File transfer is really slow!** Only around **90-350 KB/s** depending on the server load.
- **Only Linux and FreeBSD VMs** are supported.

## Syntax
```
usage: qm-file [-h] [-v] [--no-progress] [--no-checks] [--verify] vmid {put,fetch} file_in file_out

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
$ ./qm-file -vv 100 put ./bin.file /tmp/file.bin
2025-01-12 09:12:31 [INFO] Guest agent is installed and reachable.
2025-01-12 09:12:31 [INFO] OS check passed: name='debian gnu/linux', kernel-version='#1 smp preempt_dynamic debian 6.1.119-1 (2024-11-22)'.
2025-01-12 09:12:32 [INFO] Command 'cat' is available.
2025-01-12 09:12:33 [INFO] Command 'dd' is available.
2025-01-12 09:12:34 [INFO] Command 'stat' is available.
2025-01-12 09:12:35 [INFO] Command 'base64' is available.
2025-01-12 09:12:36 [INFO] Command 'sha256sum' is available.
2025-01-12 09:12:36 [INFO] Starting operation: put
2025-01-12 09:12:36 [INFO] File size: 5000000 bytes. Number of chunks: 5.
2025-01-12 09:12:36 [WARNING] File will be transferred in 5 chunks due to its size.
2025-01-12 09:12:36 [INFO] Transferring chunk of size 1048575 bytes (1/5).
2025-01-12 09:12:39 [INFO] Transferring chunk of size 1048575 bytes (2/5).
2025-01-12 09:12:42 [INFO] Transferring chunk of size 1048575 bytes (3/5).
2025-01-12 09:12:46 [INFO] Transferring chunk of size 1048575 bytes (4/5).
2025-01-12 09:12:49 [INFO] Transferring chunk of size 805700 bytes (5/5).
2025-01-12 09:12:51 [INFO] File: ./bin.file (5000000 bytes). Transfer completed, in 14.9 s (327.5 KB/s)
2025-01-12 09:12:52 [INFO] Got sha256 checksum from remote file: e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d
2025-01-12 09:12:52 [INFO] Got sha256 checksum from local file:  e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d
```

### Downloading a File from a VM
```bash
$ ./qm-file -vv 100 fetch /tmp/file.bin file.bin
2025-01-12 09:11:19 [INFO] Guest agent is installed and reachable.
2025-01-12 09:11:19 [INFO] OS check passed: name='debian gnu/linux', kernel-version='#1 smp preempt_dynamic debian 6.1.119-1 (2024-11-22)'.
2025-01-12 09:11:20 [INFO] Command 'cat' is available.
2025-01-12 09:11:21 [INFO] Command 'dd' is available.
2025-01-12 09:11:22 [INFO] Command 'stat' is available.
2025-01-12 09:11:23 [INFO] Command 'base64' is available.
2025-01-12 09:11:24 [INFO] Command 'sha256sum' is available.
2025-01-12 09:11:24 [INFO] Starting operation: fetch
2025-01-12 09:11:25 [INFO] File size: 5000000 bytes. Number of chunks: 3.
2025-01-12 09:11:25 [WARNING] File will be fetched in 3 chunks due to its size.
2025-01-12 09:11:25 [INFO] Transferring chunk of size 2097152 bytes (1/3).
2025-01-12 09:11:45 [INFO] Transferring chunk of size 2097152 bytes (2/3).
2025-01-12 09:12:06 [INFO] Transferring chunk of size 2097152 bytes (3/3).
2025-01-12 09:12:12 [INFO] File: /tmp/file.bin (5000000 bytes). Transfer completed, in 47.1 s (103.8 KB/s)
2025-01-12 09:12:13 [INFO] Got sha256 checksum from remote file: e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d
2025-01-12 09:12:13 [INFO] Got sha256 checksum from local file:  e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d
```
