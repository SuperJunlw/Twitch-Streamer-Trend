from flask import Flask
from flask import render_template
from flask import request

# modules needed to generate figure 
import base64
from io import BytesIO

import sys
#sys.path.append("../CS122")
sys.path.append('C:/Users/60298/Downloads/CS122/Project/Twitch-Streamer-Trend')
import draw_chart as dc
import prediction as pd
import read_data as rd

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")


@app.route("/current", methods=["GET"])
def current_trend():
    streamer_names = rd.get_streamer_names()
    fig = dc.draw_bar_graph(rd.get_top10_popularity())
    data = generate_plot(fig)
    return render_template("plot.html", img=f"<img src='data:image/png;base64,{data}'/>",streamer_names=streamer_names)


@app.route("/forecast")
def forecast():
    streamer_names = rd.get_streamer_names()
    try:
        months = int(request.args["months"])
        option = request.args["streamers"]
        if option == 'All':
            fig = dc.draw_future_trends(pd.predict_popularity(months), months)
        else:
            fig = dc.draw_future_trend_uno(pd.predict_popularity(months), months, option)
        data = generate_plot(fig)
        return render_template("plot.html", img=f"<img src='data:image/png;base64,{data}'/>", streamer_names=streamer_names)
    except:
        return render_template("plot.html", streamer_names=streamer_names)
    
@app.route("/historical")
def historical():
    streamer_names = rd.get_streamer_names()
    streamer_names.pop(0)
    try:
        option = request.args["streamers"]
        stats = rd.get_streamer_history(option)
        return render_template("historical.html", stats=stats, streamer_names=streamer_names, option=option)
    except:
        return render_template("historical.html", streamer_names=streamer_names)

# Apparently it's not recommanded to use mathplotlib.pyplot in Flask
# More details on https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
# This code came from the website
def generate_plot(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png",bbox_inches='tight')
    return base64.b64encode(buf.getbuffer()).decode("ascii")


if __name__ == "__main__":
    app.run()