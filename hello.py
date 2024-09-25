from datetime import datetime, UTC

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, ValidationError

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config["SECRET_KEY"] = "jk6L$G%#c9^0LC"


def utoronto_check(form, field):
    # No @ will be handled by email validator, required to avoid index error in other if statement
    if "@" not in field.data:
        return

    if "utoronto" not in field.data.split("@")[1]:
        raise ValidationError("Please use your U of T email.")


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[InputRequired()])
    email = StringField(
        "What is your U of T email?",
        validators=[InputRequired(), Email(), utoronto_check],
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        session["name"] = form.name.data
        session["email"] = form.email.data
        form.name.data = ""
        form.email.data = ""
        return redirect(url_for("index"))
    return render_template(
        "index.html", form=form, name=session.get("name"), email=session.get("email")
    )


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name, current_time=datetime.now(UTC))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
