from flask import Flask, jsonify
import signal
import sys

app = Flask(__name__)

@app.route('/api/adblock', methods=['GET'])
def adblock():
    return jsonify({"status": "ad-blocking enabled", "script": "adblock.js"})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "running"})

def graceful_shutdown(sig, frame):
    print(f'Received signal {sig}. Shutting down gracefully...')
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)