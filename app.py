from flask import Flask, render_template, jsonify, request
import subprocess
import os
from datetime import datetime
import shlex

#just run "python app.py" in the "clean md" folder and it will work!


app = Flask(__name__)

# Log file for storing all commands and outputs
LOG_FILE = "terminal_output_log.txt"
current_folder = os.getcwd()
is_wsl = False  # Flag to check if we're using a WSL path

# Helper function to convert Windows paths to WSL-compatible paths
def convert_to_wsl_path(folder):
    """
    Convert a Windows UNC path (\\wsl.localhost\...) to a valid WSL Linux path.
    """
    try:
        result = subprocess.run(f"wsl wslpath '{folder}'", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        print(f"WSL path conversion error: {e}")
        return None



def execute_and_log(command):
    """
    Executes a command in the appropriate environment (Windows or WSL).
    """
    global current_folder, is_wsl
    try:
        if is_wsl:
            # Execute the command in WSL with the converted path
            safe_command = shlex.quote(command)
            wsl_command = f"wsl bash -c \"cd '{current_folder}' && {safe_command}\""
            result = subprocess.run(wsl_command, shell=True, text=True, capture_output=True)
        else:
            # Execute Windows commands
            result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=current_folder)
        
        # Log results
        output = f"Command: {command}\nOutput:\n{result.stdout}\nError:\n{result.stderr}\n{'='*40}\n"
        with open(LOG_FILE, "a") as file:
            file.write(f"Timestamp: {datetime.now()}\n{output}")
        return {"command": command, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"command": command, "stdout": "", "stderr": str(e)}

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')




@app.route('/set_folder', methods=['POST'])
def set_folder():
    """
    Updates the current working directory, supporting both Windows and WSL paths.
    """
    global current_folder, is_wsl
    data = request.get_json()
    folder = data.get('folder', '')

    # Handle WSL UNC paths
    if folder.startswith("\\\\wsl.localhost") or folder.startswith("\\\\wsl$"):
        converted_folder = convert_to_wsl_path(folder)
        if converted_folder:
            current_folder = converted_folder
            is_wsl = True
            return jsonify({"status": "success", "folder": current_folder})
        return jsonify({"status": "error", "message": "Invalid or inaccessible WSL folder path."})

    # Handle standard Windows paths
    if os.path.exists(folder) and os.path.isdir(folder):
        current_folder = os.path.abspath(folder)
        is_wsl = False
        return jsonify({"status": "success", "folder": current_folder})
    else:
        return jsonify({"status": "error", "message": "Invalid folder path."})


# Category 1 routes with sample Bash commands
@app.route('/function1_1', methods=['GET'])
def function1_1():
    result = execute_and_log("ls -la")
    return jsonify(result)

@app.route('/function1_2', methods=['GET'])
def function1_2():
    result = execute_and_log("pwd")
    return jsonify(result)

# Category 2 routes
@app.route('/function2_1', methods=['GET'])
def function2_1():
    result = execute_and_log("echo 'Hello World!'")
    return jsonify(result)

@app.route('/function2_2', methods=['GET'])
def function2_2():
    result = execute_and_log("dir")
    return jsonify(result)

# Category 3 routes
@app.route('/function3_1', methods=['GET'])
def function3_1():
    result = execute_and_log("uname -a")
    return jsonify(result)

@app.route('/function3_2', methods=['GET'])
def function3_2():
    result = execute_and_log("df -h")
    return jsonify(result)

# Serve the log file content
@app.route('/view_log')
def view_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            content = file.read()
        return jsonify({"log": content})
    else:
        return jsonify({"log": "No log file found."})

if __name__ == '__main__':
    app.run(debug=True)
