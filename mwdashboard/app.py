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

                {
                    "name": "Google",
                    "url": "https://google.com"
                },

                {
                    "name": "YouTube",
                    "url": "https://youtube.com"
                },

                {
                    "name": "GitHub",
                    "url": "https://github.com"
                },

                {
                    "name": "Stack Overflow",
                    "url": "https://stackoverflow.com"
                },

                {
                    "name": "Reddit",
                    "url": "https://reddit.com"
                },

                {
                    "name": "Amazon",
                    "url": "https://amazon.com"
                },

                {
                    "name": "Microsoft",
                    "url": "https://microsoft.com"
                },

                {
                    "name": "OpenAI",
                    "url": "https://openai.com"
                },

                {
                    "name": "Apple",
                    "url": "https://apple.com"
                },

                {
                    "name": "Flutter",
                    "url": "https://flutter.dev"
                }

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

        elapsed = round(

            (time.time() - start) * 1000

        )

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

        for website in websites:

            url = website["url"]

            name = website["name"]

            results[url] = ping_site(url)

            results[url]["name"] = name

        # cleanup removed websites

        for site in list(results.keys()):

            exists = False

            for website in websites:

                if website["url"] == site:

                    exists = True

            if not exists:

                results.pop(site)

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

    global results

    name = request.json["name"].strip()

    url = request.json["url"].strip()

    if not name or not url:

        return jsonify({

            "success": False

        })

    data = load_websites()

    exists = False

    for website in data["websites"]:

        if website["url"] == url:

            exists = True

    if not exists:

        website = {

            "name": name,

            "url": url

        }

        data["websites"].append(

            website

        )

        save_websites(data)

        results[url] = ping_site(url)

        results[url]["name"] = name

    return jsonify({

        "success": True

    })


@app.route("/remove", methods=["POST"])
def remove_site():

    global results

    url = request.json["url"]

    data = load_websites()

    data["websites"] = [

        site

        for site in data["websites"]

        if site["url"] != url

    ]

    save_websites(data)

    results.pop(url, None)

    return jsonify({

        "success": True

    })


@app.route("/interval", methods=["POST"])
def update_interval():

    minutes = int(

        request.json["minutes"]

    )

    data = load_websites()

    data["interval"] = minutes * 60

    save_websites(data)

    return jsonify({

        "success": True

    })


if __name__ == "__main__":

    data = load_websites()

    for website in data["websites"]:

        url = website["url"]

        name = website["name"]

        results[url] = ping_site(url)

        results[url]["name"] = name

    thread = threading.Thread(

        target=monitor_loop,

        daemon=True

    )

    thread.start()

    app.run(

        debug=False,

        host="0.0.0.0",

        port=5000

    )
