from flask import Flask, render_template
from datashows import Shows

app = Flask(__name__)

Shows = Shows()

@app.route('/')
def index():
    return render_template("index.html", title="Home-")
@app.route("/about")
def about():
    return render_template("About.html", title="About-")
@app.route("/shows")
def shows():
    return render_template("shows.html", title="Shows-", Shows = Shows)
@app.route("/music")
def music():
    return render_template("Music.html", title="Music-")
@app.route("/store")
def store():
    return render_template("store/store.html", title="Store-")
@app.route("/photos")
def photos():
    return render_template("Photos.html", title="Photos-")
@app.route("/store/shirts")
def shirts():
    return render_template("store/shirts.html", title="Store-")
@app.route("/store/outwear")
def outwear():
    return render_template("store/outwear.html", title="Store-")
@app.route("/store/womens")
def womens():
    return render_template("store/womens.html", title="Store-")
@app.route("/store/accessories")
def accessories():
    return render_template("store/accessories.html", title="Store-")
@app.route("/store/cart")
def cart():
    return render_template("store/cart.html", title = "Store-")
@app.route("/about/taylor")
def tatylor():
    return render_template("about/taylor.html", title = "About-")
@app.route("/about/long")
def long():
    return render_template("about/long.html", title = "About-")
@app.route("/about/welsh")
def welsh():
    return render_template("about/long.html", title = "About-")
@app.route("/about/mckenzie")
def mckenzie():
    return render_template("about/mckenzie.html", title ="About-")
@app.route("/about/savage")
def savage():
    return render_template("about/savage.html", title = "About-")


if __name__ == '__main__':
    app.run()
