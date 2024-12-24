from flask import Flask, request, request, jsonify, render_template
import socket
import subprocess
import os

app = Flask(__name__)


@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

# Function to send a command to a terminal. 
@app.route('/execute_terminal', methods=['POST'])
def execute_command_terminal():
    data = request.json
    command = data.get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400
    else:
        print("command sent to app.py to be run by a terminal: <" + command +">")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)#command execution!
        return jsonify({'output': "EXCECUTED COMMAND: <" + command+">"})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Command failed', 'details': e.stderr}), 500
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500



# Function to send a script to the vmd console, available as a socket
@app.route('/execute_vmdconsole', methods=['POST'])
def execute_command_vmdconsole():
    data = request.json
    scriptlocation = data.get('scriptlocation')

    if not scriptlocation:
        return jsonify({'error': 'No script location provided'}), 400
    else:
        print("script location sent to app.py to be exectuted in vmd console: <" + scriptlocation +">")

    try:
        '''
        #read a text file, and return a list of the lines in the file, ignoring empty lines and lines starting with #
        with open(scriptlocation, 'r') as file:
            commands = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]

        #go thought that liset
        for command in commands:
            #send one line to vmd socked
            with socket.create_connection(("localhost", 5555)) as sock:
                sock.sendall(command.encode('utf-8') + b'\n')
                response = sock.recv(1024)
                print("Response:", response.decode('utf-8'))
        '''
        with socket.create_connection(("localhost", 5555)) as sock:
            command = "source " + scriptlocation
            sock.sendall(command.encode('utf-8') + b'\n')
            response = sock.recv(1024)
            print("Response:", response.decode('utf-8'))

        return jsonify({'output': "EXCECUTED SCRIPT: <" + scriptlocation +">"})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Command failed', 'details': e.stderr}), 500
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True, port=5000)
