from flask import Flask, render_template, request, jsonify
import requests
import threading
import time
import json
from datetime import datetime

app = Flask(__name__)

CONFIG_FILE = "websites.json"

DEFAULT_INTERVAL = 600

results = {}


def load_websites():

    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    except:

        data = {
            "interval": DEFAULT_INTERVAL,

            "websites": [

                "https://google.com",
                "https://youtube.com",
                "https://github.com",
                "https://stackoverflow.com",
                "https://reddit.com",
                "https://amazon.com",
                "https://microsoft.com",
                "https://openai.com",
                "https://apple.com",
                "https://flutter.dev"

            ]
        }

        save_websites(data)

        return data


def save_websites(data):

    with open(CONFIG_FILE, "w") as f:

        json.dump(data, f, indent=4)


def ping_site(url):

    try:

        start = time.time()

        response = requests.get(

            url,
            timeout=10,
            headers={
                "User-Agent": "WebsiteMonitor"
            }

        )

        elapsed = round((time.time() - start) * 1000)

        return {

            "status": "ONLINE",

            "status_code": response.status_code,

            "response_time": elapsed,

            "last_checked": datetime.now().strftime("%H:%M:%S")

        }

    except Exception:

        return {

            "status": "OFFLINE",

            "status_code": "-",

            "response_time": "-",

            "last_checked": datetime.now().strftime("%H:%M:%S")

        }


def monitor_loop():

    global results

    while True:

        data = load_websites()

        interval = data["interval"]

        websites = data["websites"]

        for site in websites:

            results[site] = ping_site(site)

        time.sleep(interval)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/status")
def status():

    return jsonify(results)


@app.route("/config")
def config():

    return jsonify(load_websites())


@app.route("/add", methods=["POST"])
def add_site():

    url = request.json["url"]

    data = load_websites()

    if url not in data["websites"]:

        data["websites"].append(url)

        save_websites(data)

    return jsonify({"success": True})


@app.route("/remove", methods=["POST"])
def remove_site():

    url = request.json["url"]

    data = load_websites()

    if url in data["websites"]:

        data["websites"].remove(url)

        save_websites(data)

        results.pop(url, None)

    return jsonify({"success": True})


@app.route("/interval", methods=["POST"])
def update_interval():

    minutes = int(request.json["minutes"])

    data = load_websites()

    data["interval"] = minutes * 60

    save_websites(data)

    return jsonify({"success": True})


if __name__ == "__main__":

    thread = threading.Thread(
        target=monitor_loop,
        daemon=True
    )

    thread.start()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )