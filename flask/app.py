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
import read_data as rd

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")


@app.route("/current", methods=["GET"])
def current_trend():
    fig = dc.draw_bar_graph(rd.get_top10_popularity())
    data = generate_plot(fig)
    return render_template("current.html", img=f"<img src='data:image/png;base64,{data}'/>")


@app.route("/forecast")
def forecast():
    try:
        months = int(request.args["months"])
        fig = dc.draw_future_trends(pd.predict_popularity(months), months)
        data = generate_plot(fig)
        return render_template("current.html", img=f"<img src='data:image/png;base64,{data}'/>")
    except:
        return render_template("current.html")


# Apparently it's not recommanded to use mathplotlib.pyplot in Flask
# More details on https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
# This code came from the website
def generate_plot(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


if __name__ == "__main__":
    app.run()