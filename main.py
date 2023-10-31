from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField("Cafe name", validators=[DataRequired()])
    location_url = StringField("Location URL", validators=[DataRequired(), URL()])
    open_time = StringField("Open time", validators=[DataRequired()])
    closing_time = StringField("Closing time", validators=[DataRequired()])
    coffee_rating = SelectField(
        "Coffee rating",
        validators=[DataRequired()],
        choices=["✘", "☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
    )
    wifi_rating = SelectField(
        "Wifi rating",
        validators=[DataRequired()],
        choices=["💪💪💪💪💪", "💪💪💪💪", "💪💪💪", "💪💪", "💪", "✘"],
    )
    power_rating = SelectField(
        "Power rating",
        validators=[DataRequired()],
        choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
    )
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    values = []
    attribute = [
        "cafe",
        "location_url",
        "open_time",
        "closing_time",
        "coffee_rating",
        "wifi_rating",
        "power_rating",
    ]
    for key, value in form.data.items():
        if key in attribute:
            values.append(value)
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(values)
        return render_template("index.html")
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", newline="") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


if __name__ == "__main__":
    app.run(debug=True)
