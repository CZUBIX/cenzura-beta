import flask
import json
import os
from bs4 import BeautifulSoup
import random
import requests
import lxml
import cchardet

url = "https://discord.com/api/v8"
app = flask.Flask(__name__)
requests_session = requests.Session()

@app.route("/", methods=["GET"])
def main():
    return flask.render_template("index.html")

@app.route("/discord", methods=["GET"])
def discord():
    return flask.redirect("https://discord.gg/kJuGceekR5")

@app.route("/invite", methods=["GET"])
def invite():
    return flask.redirect("https://discord.com/api/oauth2/authorize?client_id=705552952600952960&permissions=268561494&scope=bot")

@app.route("/sourcecode", methods=["GET"])
def sourcecode():
    return flask.redirect("https://github.com/CZUBIX/cenzura")

@app.route("/docs", methods=["GET"])
def docs():
    with open("/cenzurabeta/commands.json", "r") as f:
        commands = json.load(f)

    blacklist = ["help", "dev"]

    categories = {}
    for command in commands:
        commands[command]["name"] = command
        if not commands[command]["category"] in categories:
            categories[commands[command]["category"]] = []

    for command in commands:
        categories[commands[command]["category"]].append(commands[command])

    for category in blacklist:
        del categories[category]

    return flask.render_template("docs.html", categories=categories)

@app.route("/api/memes", methods=["GET"])
def memes():
    jbzd = []
    kwejk = []

    while not jbzd:
        jbzd_page = requests_session.get(f"https://jbzd.com.pl/str/{random.randint(1, 235)}").content
        jbzd_soup = BeautifulSoup(jbzd_page, "lxml")

        jbzd = jbzd_soup.find_all("img", {"class":"article-image"})
        jbzd = [meme["src"] for meme in jbzd]

    while not kwejk:
        kwejk_page = requests_session.get(f"https://kwejk.pl/strona/{random.randint(4, 4000)}").content
        kwejk_soup = BeautifulSoup(kwejk_page, "lxml")

        kwejk = kwejk_soup.find_all("img", {"class":"full-image"})
        kwejk = [meme["src"] for meme in kwejk]

    return flask.jsonify({
        "jbzd": random.choice(jbzd),
        "kwejk": random.choice(kwejk)
    })

@app.route("/sitemap.xml")
def sitemap():
    return flask.send_from_directory("./", "sitemap.xml")

@app.route("/robots.txt")
def robots():
    return flask.send_from_directory("./", "robots.txt")

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)

    return flask.url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2137)
