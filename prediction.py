import ast

import numpy as np
import read_data as rd
import os

def compute_trends(top10Streamers):

    streamer_trends = []
    min_max = rd.get_normal_min_max()

    for streamer in top10Streamers:
        # first element is the streamer name, second is the trend/changes in popularity, third is the current popularity
        streamer_trends.append((streamer[0], compute_streamer_trend(streamer[0], min_max), streamer[1]))

    return streamer_trends


def compute_streamer_trend(name, min_max):
    s_name = name + '.txt'
    filepath = os.path.join('streamers2', s_name)

    with open(filepath, 'r') as file:
        contents = file.read()

    contents = contents.split('\n')[:-1]

    popularity_each_days = []

    for line in contents:
        stat = ast.literal_eval(line)
        popularity_each_days.append(rd.compute_popularity(stat, min_max))

    p_array = np.array(popularity_each_days)
    day_array = np.arange(1, len(contents)+1)
    coefficients = np.polyfit(day_array, p_array, 1)
    
    return coefficients[0]

def predict_popularity(num_month):
    top10_trends = compute_trends(rd.get_top10_popularity())
    predicted_popularity = []
    #print(top10_trends)
    for streamer in top10_trends:
        prediction = num_month * streamer[1] + streamer[2]
        predicted_popularity.append((streamer[0], prediction))

    return predicted_popularity

print(predict_popularity(3))

