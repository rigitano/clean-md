from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def run_script():
    script = request.args.get('script', '')
    if script:
        # Adjust the command below for Tcl or Python execution in VMD
        command = f"vmd -e {script}"
        subprocess.run(command, shell=True)
        return f"Executed {script}", 200
    return "No script specified", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
