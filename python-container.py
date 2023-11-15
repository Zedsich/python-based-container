# A simple realization of container based on python

import os
import subprocess
import sys

def run():
    print(f"Running {sys.argv[2:]}")

    script_path = os.path.abspath(sys.argv[0])
    python_interpreter = sys.executable

    cmd = [python_interpreter, script_path, "child"] + sys.argv[2:]
    subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def child():
    print(f"Running {sys.argv[2:]}")

    cg()

    cmd = sys.argv[2:]
    subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    # Clean up
    subprocess.run(["umount", "proc"])
    subprocess.run(["umount", "thing"])

def cg():
    cgroups = "/sys/fs/cgroup/"
    pids = os.path.join(cgroups, "pids")
    os.makedirs(os.path.join(pids, "zed"), exist_ok=True)

    with open(os.path.join(pids, "zed/pids.max"), "w") as f:
        f.write("20")

    # Removes the new cgroup in place after the container exits
    with open(os.path.join(pids, "zed/notify_on_release"), "w") as f:
        f.write("1")

    with open(os.path.join(pids, "zed/cgroup.procs"), "w") as f:
        f.write(str(os.getpid()))

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py run <cmd> <args>")
        sys.exit(1)

    if sys.argv[1] == "run":
        run()
    elif sys.argv[1] == "child":
        child()
    else:
        print("Invalid command")
        sys.exit(1)

if __name__ == "__main__":
    main()
