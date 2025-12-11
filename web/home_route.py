from flask import Blueprint, redirect

site_prefix = __name__.split(".")[-1]

app = Blueprint(site_prefix, __name__)


@app.route("/")
def home():
    return redirect("/static/kerk_naam1/kerk_naam1_iframes.html")

