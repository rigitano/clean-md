from flask import Flask, render_template, jsonify, request
import subprocess
import os
from datetime import datetime

#just run "python app.py" in the "clean md" folder and it will work!


app = Flask(__name__)

# Log file for storing all commands and outputs
LOG_FILE = "terminal_output_log.txt"

# Utility function to execute a Bash command and log it
def execute_and_log(command):
    try:
        # Run the Bash command and capture the output
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        output = f"Command: {command}\nOutput:\n{result.stdout}\nError:\n{result.stderr}\n{'='*40}\n"

        # Log to a file
        with open(LOG_FILE, "a") as file:
            file.write(f"Timestamp: {datetime.now()}\n{output}")

        # Return the result to the front-end
        return {"command": command, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        error_message = f"Error executing command: {str(e)}"
        return {"command": command, "stdout": "", "stderr": error_message}

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

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
    result = execute_and_log("date")
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
