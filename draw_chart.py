import numpy as np
import read_data as rd
import prediction as pd
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

def draw_bar_graph(top10_popularity):
    sorted_popularity = sorted(top10_popularity, key=lambda x: x[1], reverse=True)

    streamer_names = [n[0] for n in sorted_popularity]
    streamer_popularities = [p[1] for p in sorted_popularity]
    colors = ['yellowgreen','orchid', 'lime', 'violet', 'lightgreen', 'olive', 'grey','teal', 'salmon', 'tan']

    fig = Figure(figsize=(10,8))
    ax = fig.subplots()
    ax.bar(streamer_names, streamer_popularities, color=colors)

    fig.supxlabel('Streamers', y=0.05)
    fig.supylabel('Popularity', x=0.05)
    fig.suptitle('Current Top 10 Twitch Streamers and Their Popularity', y=0.91)

    for i, name in enumerate(streamer_names):
        ax.text(i, streamer_popularities[i], name, ha='center', va='bottom', rotation=45)

    ax.set_xticks([])
    #plt.yticks([min(streamer_popularities), max(streamer_popularities)], ["Less Popular", "Most Popular"])

    ax.set_ylim(0, max(streamer_popularities) +0.08)
    return fig


def draw_future_trends(top10_predication, num_month):
    colors = ['yellowgreen','orchid', 'lime', 'violet', 'lightgreen', 'olive', 'grey','teal', 'salmon', 'tan']
    months = np.arange(0, num_month+1, 1)
    i = 0

    fig = Figure(figsize=(10,8))
    ax = fig.subplots()

    for streamer in top10_predication:
        future_trend = np.array(streamer[2])
        ax.plot(months, future_trend, label=streamer[0], color=colors[i])
        i += 1


    fig.supxlabel('Each Month from Now', y=0.05)
    fig.supylabel('Popularity', x=0.05)
    fig.suptitle('Popularity of Current Top 10 Twitch Streamers in the future', y=0.91)

    fig.legend(loc="center right", bbox_to_anchor=(1.05, .5))
    return fig

draw_bar_graph(rd.get_top10_popularity())
