#!/bin/python3

import sys
import subprocess
import os
import json
import base64
import time
import argparse


PROGRESS_BAR = True
VERBOSE = False


def read_in_chunks(file_path, chunk_size):
    """Reads a file in chunks of the specified size."""
    with open(file_path, 'rb') as file:  # Open in binary mode to handle all file types
        while chunk := file.read(chunk_size):
            yield chunk


def print_progress_bar(iteration, total, elapsed_time, transferred_bytes, length=50):
    """Prints a progress bar with transfer rate to the console."""
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '=' * filled_length + '-' * (length - filled_length)
    rate = transferred_bytes / (1024 * elapsed_time) if elapsed_time > 0 else 0  # MB/s
    print(f"\rProgress: |{bar}| {percent}% Complete | {rate:.2f} KB/s", end="\r")
    if iteration == total:
        print()  # Move to a new line on completion


def qm_exec(vmid, cmd, data_in = None):
    output = None
    text = None
    try:
        call = ["qm", "guest", "exec", vmid]
        if data_in:
            text = False
            call = call + ["--pass-stdin", "1"]
        call = call + ["--"] + cmd
        if VERBOSE:
            print('[DEBUG] call: ' + ' '.join(call), file=sys.stderr)
        if os.getuid() != 0:
            call = ["sudo"] + call
        process = subprocess.run(call,
            input=data_in,
            text=text,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    stdout=process.stdout.decode()
    stderr=process.stderr.decode()

    if VERBOSE:
        print(f'[DEBUG] stdout: {stdout}', file=sys.stderr)
        print(f'[DEBUG] stderr: {stdout}', file=sys.stderr)

    if not stdout:
        print(stdout)
        print(stderr, file=sys.stderr)
        sys.exit(1)

    stdout_json = json.loads(stdout)

    if stdout_json['exitcode'] != 0 or stdout_json['exited'] != 1:
        print(stdout)
        print(stderr, file=sys.stderr)
        sys.exit(1)

    if 'out-data' in stdout_json:
        output = stdout_json['out-data']

    return output


def qm_put(vmid, file_in, file_out, chunk_size):
    file_size = os.path.getsize(file_in)  # Get the total file size
    total_chunks = (file_size + chunk_size - 1) // chunk_size  # Calculate the total number of chunks
    operator = '>'
    if PROGRESS_BAR:
        current_chunk = 0
        transferred_bytes = 0
        start_time = time.time()
        print_progress_bar(current_chunk, total_chunks, 0, transferred_bytes)

    for chunk in read_in_chunks(file_in, chunk_size):
        qm_exec(vmid, ["sh", "-c", f"cat {operator} {file_out}"], data_in=chunk)
        operator = '>>'
        if PROGRESS_BAR:
            current_chunk += 1
            transferred_bytes += len(chunk)
            elapsed_time = time.time() - start_time
            print_progress_bar(current_chunk, total_chunks, elapsed_time, transferred_bytes)


def qm_fetch(vmid, file_in, file_out, chunk_size):
    file_size = int(qm_exec(vmid, ["sh", "-c", f'stat --printf="%s" {file_in}']))
    total_chunks = (file_size + chunk_size - 1) // chunk_size  # Calculate the total number of chunks
    if PROGRESS_BAR:
        start_time = time.time()
        print_progress_bar(0, total_chunks, 0, 0)

    with open(file_out, 'wb') as fid:
        for current_chunk in range(0, total_chunks):
            fid.write(
                base64.b64decode(
                    qm_exec(
                        vmid,
                        [
                            "sh", "-c",
                            f"dd if={file_in} bs=1024 count={int(chunk_size/1024)} skip={current_chunk} | base64 -w 0"
                        ])))
            if PROGRESS_BAR:
                if file_size - transferred_bytes >= chunk_size:
                    transferred_bytes += chunk_size
                else:
                    transferred_bytes = file_size
                elapsed_time = time.time() - start_time
                print_progress_bar(current_chunk + 1, total_chunks, elapsed_time, transferred_bytes)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Put / Fetch file in chunks from / to a VM.")
    parser.add_argument("vmid", help="VM ID")
    parser.add_argument("mode", help="Transfer mode", choices=['put', 'fetch'])
    parser.add_argument("file_in", help="Path of input file")
    parser.add_argument("file_out", help="Path of output file")
    parser.add_argument("-v", "--verbose", help="Show verbose output", action='store_true')
    parser.add_argument("--no-progress", help="Don't show progress", action='store_true')

    args = parser.parse_args()
    
    if args['verbose']:
        VERBOSE = True
    if args['no-progress']:
        PROGRESS_BAR = False

    chunk_size = (1024 * 1024)  # 1 MiB

    if args.mode == 'put':
        qm_put(args.vmid, args.file_in, args.file_out, chunk_size -1)

    if args.mode == 'fetch':
        qm_fetch(args.vmid, args.file_in, args.file_out, chunk_size)

if __name__ == "__main__":
    main()
