import numpy as np
import read_data as rd
import prediction as pd
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

# Create a bar graph to display the current top 10 streamer's scores
def draw_bar_graph(top10_popularity):
    sorted_popularity = sorted(top10_popularity, key=lambda x: x[1], reverse=True)

    # sort streamer names and scores from larget to smallest
    streamer_names = [n[0] for n in sorted_popularity]
    streamer_popularities = [p[1] for p in sorted_popularity]
    colors = ['yellowgreen','orchid', 'lime', 'violet', 'lightgreen', 'olive', 'grey','teal', 'salmon', 'tan']

    fig = Figure(figsize=(10,8))
    ax = fig.subplots()
    ax.bar(streamer_names, streamer_popularities, color=colors)

    fig.supxlabel('Streamers', y=0.05)
    fig.supylabel('Popularity', x=0.05)
    fig.suptitle('Current Top 10 Twitch Streamers and Their Popularity', y=0.91)

    # add names as labels for each bar
    for i, name in enumerate(streamer_names):
        ax.text(i, streamer_popularities[i], name, ha='center', va='bottom', rotation=45)

    ax.set_xticks([])

    ax.set_ylim(0, max(streamer_popularities) +0.08) # set range of y
    return fig


# Create a plot with trend lines of all the top 10 streamers
def draw_future_trends(top10_predication, num_month):
    colors = ['yellowgreen','orchid', 'lime', 'violet', 'lightgreen', 'olive', 'grey','teal', 'salmon', 'tan']
    months = np.arange(0, num_month+1, 1)
    i = 0

    fig = Figure(figsize=(10,8))
    ax = fig.subplots()

    # plot trend line for every streamer
    for streamer in top10_predication:
        future_trend = np.array(streamer[2])
        ax.plot(months, future_trend, label=streamer[0] + ': ' + '{:.4f}'.format(streamer[3]) + ' Popularity/Month', color=colors[i])
        i += 1

    fig.supxlabel('Each Month from Now', y=0.05)
    fig.supylabel('Popularity', x=0.05)
    fig.suptitle('Popularity of Current Top 10 Twitch Streamers in the future', y=0.91)

    fig.legend(loc="center right", bbox_to_anchor=(1.3, .5))
    return fig


# plot trend line for one streamer based on the name passed to the function
def draw_future_trend_uno(top10_predication, num_month, name):
    months = np.arange(0, num_month+1, 1)

    fig = Figure(figsize=(10,8))
    ax = fig.subplots()

    trends = []

    # Get a list of the predicted score of all the streamer
    # use for the range of y in the plot, to keep the range same for all streamers
    for streamer in top10_predication:
        trends.append(streamer[1])

    for streamer in top10_predication:
        # Find the streamer that user want, then plot the trend line
        if streamer[0] == name:
            future_trend = np.array(streamer[2])
            ax.plot(months, future_trend, label=streamer[0] + ': ' + '{:.4f}'.format(streamer[3]) + ' Popularity/Month', color='blue')

            # add label and display each point
            ax.scatter(months, future_trend, color='black') 
            for i, txt in enumerate(future_trend):
                ax.text(months[i], txt, '{:.3f}'.format(txt), ha='right', va='bottom', color='black', fontsize=8)

            ax.set_ylim(0, max(trends))
            break

    fig.legend(loc="center right", bbox_to_anchor=(1.3, .5))
    fig.supxlabel('Each Month from Now', y=0.05)
    fig.supylabel('Popularity', x=0.05)
    fig.suptitle('Popularity of Current Top 10 Twitch Streamers in the future', y=0.91)

    return fig
