from flask import Flask, jsonify
import psutil
import logging
import time
import os

app = Flask(__name__)

start_time = time.time()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)

@app.route('/health')
def health():
    logging.info("/health - OK")
    return jsonify({"status": "ok"}), 200


@app.route('/uptime')
def uptime():
    uptime_seconds = int(time.time() - start_time)
    return jsonify({"uptime_seconds": uptime_seconds}), 200


@app.route('/metrics')
def metrics():
    try:
        data = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
        logging.info("/metrics - OK")
        return jsonify(data), 200

    except Exception:
        logging.exception("/metrics - ERROR")
        return jsonify({"error": "Could not fetch metrics"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)