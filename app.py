from flask import Flask, render_template, url_for

app = Flask (__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/munfunction_battery_not_hold_charge')
def munfunction_battery_not_hold_charge():
    return render_template("munfunction_battery_not_hold_charge.html")


if __name__ == "__main__":
    app.run(debug=True) #поставить false