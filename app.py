from flask import Flask, request
import socket

app = Flask(__name__)

# Function to send commands to the running VMD instance
def send_to_vmd(command):
    VMD_HOST = 'localhost'
    VMD_PORT = 5555
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((VMD_HOST, VMD_PORT))
            s.sendall(command.encode('utf-8') + b'\n')
        return f"Sent command: {command}", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/run', methods=['GET'])
def run_script():
    script_name = request.args.get('script', '')
    if script_name:
        try:
            # Load and send the script content
            with open(script_name, 'r') as file:
                script_content = file.read()
            return send_to_vmd(script_content)
        except FileNotFoundError:
            return f"Error: Script {script_name} not found", 404
    return "No script specified", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
