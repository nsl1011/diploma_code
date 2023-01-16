from flask import Flask, render_template, url_for
#import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn="https://edf95c656a5644c08e7f95753ede281a@o4504514952101888.ingest.sentry.io/4504514955313152",
#     integrations=[
#         FlaskIntegration(),
#     ],

#     traces_sample_rate=1.0
# )

app = Flask (__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/munfunction_battery_not_hold_charge')
def munfunction_battery_not_hold_charge():
    return render_template("munfunction_battery_not_hold_charge.html")


if __name__ == "__main__":
    app.run(debug=True) #поставить false