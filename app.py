from flask import Flask, request, request, jsonify, render_template
import socket
import subprocess
import os

app = Flask(__name__)


@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

# Function to send a command to a terminal. Im using only for VMD for now
@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400
    else:
        print("command sent to app.py to be run: <" + command +">")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)#command execution!
        return jsonify({'output': "EXCECUTED COMMAND:" + command})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Command failed', 'details': e.stderr}), 500
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
