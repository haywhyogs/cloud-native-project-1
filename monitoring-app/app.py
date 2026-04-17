from flask import Flask, jsonify
import psutil
import logging
import time
import os
import requests

APP_NAME = "monitoring-app"
APP_VERSION = "v4"

SERVICES = {
    "container 1": "http://52.156.1.70:5000/health",
    "container 2": "http://52.156.1.70:5001/health",
    "container 3": "http://52.156.1.70:5002/health"
}

app = Flask(__name__)

logging.info(f"Starting {APP_NAME} version {APP_VERSION}")

start_time = time.time()

# Configure logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)


@app.route("/version")
def version():
        return jsonify({
            "app": APP_NAME,
            "version": APP_VERSION
        }), 200


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
    results = {}

    for name, url in SERVICES.items():
        try:
            response = requests.get(url, timeout=2)

            results[name] = {
                "status": "reachable",
                "status_code": response.status_code
            }

        except Exception:
            logging.exception(f"/check - {name} FAILED")

            results[name] = {
                "status": "unreachable"
            }

    return jsonify(results), 200

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
        services_status = {}

        for name, url in SERVICES.items():
            try:
                response = requests.get(url, timeout=2)
                services_status[name] = {
                    "status": "reachable",
                    "status_code": response.status_code
                }
            except:
                services_status[name] = {
                    "status": "unreachable"
                }

        return jsonify({
            "app_status": "running",
            "services": services_status,
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