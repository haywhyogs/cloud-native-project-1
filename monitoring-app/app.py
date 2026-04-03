from flask import Flask, jsonify
import psutil
import logging
import time
import os
import requests

APP_NAME = "monitoring-app"
APP_VERSION = "v2"

app = Flask(__name__)

start_time = time.time()

# Configure logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)



@app.route('/health')
def health():
    logging.info("/health - OK")
    return jsonify({"status": "ok"}), 200


@app.route("/uptime")
def uptime():
    try:
        uptime_seconds = time.time() - start_time
        logging.info("/uptime - OK")

        return jsonify({
            "uptime_seconds": uptime_seconds
        }), 200

    except Exception:
        logging.exception("/uptime - ERROR")
        return jsonify({"error": "Could not fetch uptime"}), 500


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


@app.route("/check")
def check():
    try:
        logging.info("/check - Checking external service")

        response = requests.get("https://monitoring-webapp.azurewebsites.net/health")

        return jsonify({
            "service_status": "reachable",
            "status_code": response.status_code
        }), 200

    except Exception:
        logging.exception("/check - ERROR")

        return jsonify({
            "service_status": "unreachable"
        }), 500

@app.route("/status")
def status():
    try:
        logging.info("/status - Aggregating system status")

        # Self metrics
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        uptime_seconds = time.time() - start_time

        # External check
        try:
            response = requests.get("https://monitoring-webapp.azurewebsites.net/health")
            service_status = "reachable"
            status_code = response.status_code
        except:
            service_status = "unreachable"
            status_code = None

        return jsonify({
            "app_status": "running",
            "service_status": service_status,
            "status_code": status_code,
            "cpu_percent": cpu,
            "memory_percent": memory,
            "disk_percent": disk,
            "uptime_seconds": uptime_seconds,
            "timestamp": time.ctime()
        }), 200

    except Exception:
        logging.exception("/status - ERROR")
        return jsonify({"error": "Could not fetch status"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)