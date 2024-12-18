import os
import subprocess
import threading
import sys
import shutil

from flask import Flask, render_template, request, jsonify
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

# Pre-check which shells are available.
# This is platform-specific. We'll define a dictionary of known shells.
if os.name == 'nt':  # Windows
    possible_shells = {
        "bash": "bash.exe",
        "zsh": "zsh.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "wsl": "wsl.exe"
    }
else:  # Unix-like
    possible_shells = {
        "bash": "/bin/bash",
        "zsh": "/bin/zsh",
        "cmd": "cmd.exe",          # Typically not available on Unix
        "powershell": "powershell.exe",  # Typically not available on Unix
        "wsl": "wsl.exe"           # Typically not available on Unix
    }

available_shells = {}
for shell_name, shell_cmd in possible_shells.items():
    # which will return None if not found. On Windows, for some shells, it might not work as expected.
    # For Windows shells that aren't on PATH, this might fail. In that case, you can skip this check.
    # As a fallback, we trust that if user wants that shell, they have it.
    # Or we handle known Windows shells more explicitly.
    if os.name == 'nt':
        # On Windows, checking availability might be trickier. We'll just do a fallback:
        # We'll try `shutil.which()` and if None, consider it unavailable.
        if shutil.which(shell_cmd):
            available_shells[shell_name] = shell_cmd
        else:
            # Not found, skip
            available_shells[shell_name] = None
    else:
        # Unix-like: straightforward check
        if shutil.which(shell_cmd):
            available_shells[shell_name] = shell_cmd
        else:
            available_shells[shell_name] = None

if os.name == 'nt':
    import wexpect
    def create_pty(shell_command):
        return wexpect.spawn(shell_command)
else:
    import pty
    import select
    import fcntl
    import struct
    import termios

    def set_winsize(fd, rows, cols, xpix=0, ypix=0):
        winsize = struct.pack("HHHH", rows, cols, xpix, ypix)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

    def create_pty(shell_command):
        master_fd, slave_fd = pty.openpty()
        set_winsize(master_fd, 24, 80)
        pid = subprocess.Popen(shell_command, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, shell=True, preexec_fn=os.setsid)
        os.close(slave_fd)
        return master_fd, pid


@app.route('/')
def index():
    # Prepare a list of shells and mark which are unavailable
    shells_for_template = []
    for s, cmd in available_shells.items():
        # If cmd is None, shell not found
        # We'll disable that option in the dropdown
        shells_for_template.append({
            'name': s,
            'cmd': cmd if cmd else '',
            'available': (cmd is not None)
        })

    return render_template("index.html", shells=shells_for_template, hi="o",composed="echo nope")


@sock.route('/ws')
def terminal_ws(ws):
    shell = ws.receive()
    shell = shell.strip()

    # Basic shell selection logic with fallback if not available
    shell_command = available_shells.get(shell)
    if shell_command is None:
        # Shell not available, fallback to a known good shell
        if os.name == 'nt':
            shell_command = "cmd.exe"
        else:
            shell_command = "/bin/bash"

    if os.name == 'nt':
        # Windows: wexpect approach
        child = create_pty(shell_command)

        def reader():
            # Set a small timeout on the child so that read_nonblocking() will raise TIMEOUT if no data
            child.timeout = 0.05
            while True:
                try:
                    out = child.read_nonblocking(size=1024)
                    if out:
                        # wexpect returns already-decoded strings (Unicode)
                        ws.send(out)
                except wexpect.TIMEOUT:
                    continue
                except wexpect.EOF:
                    break

        reader_thread = threading.Thread(target=reader, daemon=True)
        reader_thread.start()

        while True:
            msg = ws.receive()
            if msg is None:
                break
            child.send(msg)

    else:
        # Unix-like: original pty code
        master_fd, process = create_pty(shell_command)

        def reader():
            while True:
                r, w, e = select.select([master_fd], [], [], 0.01)
                if master_fd in r:
                    try:
                        output = os.read(master_fd, 1024)
                        if output:
                            ws.send(output.decode('utf-8', 'replace'))
                        else:
                            break
                    except OSError:
                        break

        reader_thread = threading.Thread(target=reader, daemon=True)
        reader_thread.start()

        while True:
            msg = ws.receive()
            if msg is None:
                break
            os.write(master_fd, msg.encode('utf-8', 'replace'))




@app.route('/do-stuff', methods=['POST'])
def do_stuff():
    # Prepare a list of shells and mark which are unavailable
    shells_for_template = []
    for s, cmd in available_shells.items():
        # If cmd is None, shell not found
        # We'll disable that option in the dropdown
        shells_for_template.append({
            'name': s,
            'cmd': cmd if cmd else '',
            'available': (cmd is not None)
        })

    return render_template("index.html", shells=shells_for_template, hi="i",composed="echo nope")






if __name__ == '__main__':
    # You may need to adjust run parameters if using wss (TLS)
    # For local testing (ws), just run as is:
    app.run(debug=True, host='0.0.0.0', port=5000)
