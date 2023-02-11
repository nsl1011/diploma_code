from flask import Flask, render_template, url_for, request, redirect
import pymysql
from datetime import datetime
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn="https://edf95c656a5644c08e7f95753ede281a@o4504514952101888.ingest.sentry.io/4504514955313152",
#     integrations=[
#         FlaskIntegration(),
#     ],

#     traces_sample_rate=1.0
# )

app = Flask (__name__)


def db_connect():
    connect = pymysql.connect(
        host="pari2020.beget.tech",
        user="pari2020_comment",
        password="Q12345!",
        database="pari2020_comment",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connect

# connect = db_connect()
# with connect.cursor() as cursor:
#     cursor.execute("""INSERT INTO `comment` (`name`) value(%s)""", (5,))
#     cursor.execute("""DELETE FROM `comment`""")

def add_comment(comment):
    try:
        connect = db_connect()
        with connect.cursor() as cursor:
            cursor.execute("""INSERT INTO `comment` (`comment`) value(%s)""", (comment,))
    except Exception as error:
        print(f"error_add_comment {error}")
    finally:
        connect.commit()
        connect.close()


@app.route('/form_send', methods=["GET"])
def form_send():
    if request.method == "GET":
        data = request.args.get('comment_send','')
        if(len(data) > 0):
            add_comment(data)
    return redirect('/munfunction_battery_not_hold_charge')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/munfunction_battery_not_hold_charge')
def munfunction_battery_not_hold_charge():
    return render_template("munfunction_battery_not_hold_charge.html")


if __name__ == "__main__":
    app.run(debug=True) #поставить false, чтобы не было ошибокы