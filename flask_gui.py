import os

from flask import Flask
from flask import redirect
from web.kerk_naam1.routes import app as kerk_naam1
from web.home_route import app as home

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

app = Flask(__name__, static_folder='web/static')
app.register_blueprint(kerk_naam1)
app.register_blueprint(home)

print(app.url_map)

#  comment next line to run on python anywhere
app.run(debug=True, use_reloader=False, host="127.0.0.1")


@app.route("/favicon.ico")
def favicon():
    return redirect("static/favicon.png")