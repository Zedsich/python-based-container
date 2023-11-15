# A simple realization of container based on python
#     - Adapted for Cgroup v2

import os
import subprocess
import sys

def run():
    print(f"Running {sys.argv[2:]}")

    script_path = os.path.abspath(sys.argv[0])
    python_interpreter = sys.executable

    cmd = ["sudo", python_interpreter, script_path, "child"] + sys.argv[2:]
    subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def child():
    print(f"Running {sys.argv[2:]}")

    cg()

    cmd = sys.argv[2:]
    subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    # Clean up
    subprocess.run(["umount", "proc"])
    subprocess.run(["umount", "thing"])

def set_hostname(new_hostname):
    # This function will be called from within the unshare/namespace
    subprocess.run(["hostnamectl", "set-hostname", new_hostname])

def cg():
    cgroups = "/sys/fs/cgroup/"
    pids_max_path = os.path.join(cgroups, "pids.max")
    os.makedirs(pids_max_path, exist_ok=True)

    with open(os.path.join(pids_max_path, "pids.max"), "w") as f:
        f.write("20")

    with open(os.path.join(pids_max_path, "cgroup.procs"), "w") as f:
        f.write(str(os.getpid()))

def main():
    if len(sys.argv) < 2:
        print("Usage: sudo python script.py run <cmd> <args>")
        sys.exit(1)

    if sys.argv[1] == "run":
        run()
    elif sys.argv[1] == "child":
        child()
    elif sys.argv[1] == "set_hostname":
        set_hostname(sys.argv[2])
    else:
        print("Invalid command")
        sys.exit(1)

if __name__ == "__main__":
    main()
