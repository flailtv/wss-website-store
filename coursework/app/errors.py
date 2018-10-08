from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template("error_pages/404.html"), 404

#  This is where an error page is called when an error is given out
