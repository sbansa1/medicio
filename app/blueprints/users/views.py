from flask import render_template

from app.blueprints.users import user


@user.route("/")
def index():
    return render_template('index/index.html')