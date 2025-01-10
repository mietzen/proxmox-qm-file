# qm-file

`qm-file` is a Python script designed to transfer files to and from virtual machines (VMs) managed by Proxmox VE. It uses the `qm guest exec` command to execute file operations inside the VM and supports chunked file transfers for large files.

## Caveats:

- **File transfer is really slow!** Only around **90-350 KB/s** depending on the server load.
- **Only Linux and FreeBSD** are supported.

## Syntax
```
usage: qm-file [-h] [-v] [--no_progress] vmid {put,fetch} file_in file_out

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
```

## Examples

### Uploading a File to a VM
```bash
$ sha256sum file.bin
e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d  file.bin

$ qm-file 100 put file.bin /tmp/file.bin
  Progress: |==============================| 100.0% Complete | 275.68 KB/s

$ qm guest exec 1001 -- sh -c 'sha256sum /tmp/file.bin' | jq -r '."out-data"'
e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d  /tmp/file.bin
```

### Downloading a File from a VM
```bash
$ qm guest exec 1001 -- sh -c 'sha256sum /tmp/file.bin' | jq -r '."out-data"'
e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d  /tmp/file.bin

$ qm-file 100 fetch /tmp/file.bin file.bin.out
  Progress: |==============================| 100.0% Complete | 122.60 KB/s

$ sha256sum file.bin.out
e00a0f39747bdb651c28f78f2440aee87a27154c871e0b516b727a5575a8066d  file.bin.out
```
