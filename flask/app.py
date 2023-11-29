from flask import Flask
from flask import render_template
from flask import request

# modules needed to generate figure 
import base64
from io import BytesIO

import sys
sys.path.append('../CS122')
import draw_chart as dc
import prediction as pd


app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")


@app.route("/forecast", methods=["GET"])
def forecast():
    months = request.args["months"]
    data = generate_plot(int(months))
    return render_template("main.html", img=f"<img src='data:image/png;base64,{data}'/>")


# Apparently it's not recommanded to use mathplotlib.pyplot in Flask
# More details on https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
def generate_plot(months):
    fig = dc.draw_future_trends(pd.predict_popularity(months), months)

    # This code came from the website
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


if __name__ == "__main__":
    app.run()