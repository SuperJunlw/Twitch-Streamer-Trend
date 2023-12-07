import ast
import numpy as np
import read_data as rd
import os

# Return a list of tuple, tuple comtains streamer's name, trend/slope and current popularity score
def compute_trends(top10Streamers):

    streamer_trends = []
    min_max = rd.get_normal_min_max()

    for streamer in top10Streamers:

        # first element is the streamer name, second is the trend/changes in popularity, third is the current popularity
        streamer_trends.append((streamer[0], compute_streamer_trend(streamer[0], min_max), streamer[1]))

    return streamer_trends


# Use all the existed data of a streamer to compute a trend, and return the trend/slope of that steamer
def compute_streamer_trend(name, min_max):

    # read all data from a streamer's file
    s_name = name + '.txt'
    filepath = os.path.join('streamers2', s_name)

    with open(filepath, 'r') as file:
        contents = file.read()

    contents = contents.split('\n')[:-1]

    popularity_each_days = []

    # each line is a streamer's data of one day, compute the popularity score for each day
    for line in contents:
        stat = ast.literal_eval(line)
        popularity_each_days.append(rd.compute_popularity(stat, min_max))

    # use the popularity scores and numpy to compute the trend/slope of the score of a steamer
    p_array = np.array(popularity_each_days)
    day_array = np.arange(1, len(contents)+1)
    coefficients = np.polyfit(day_array, p_array, 1)
    
    return coefficients[0]


# Predict the popluarity of top 10 stremaer, return a list of tuple,
# tuple contains streamer's name, popularity in number of month, 
# a list of populrity scores each month in the coming month and current popularity score
def predict_popularity(num_month):
    top10_trends = compute_trends(rd.get_top10_popularity())

    predicted_popularity = []
  
    for streamer in top10_trends:
        # compute the popluarity score of in number of month later 
        # by adding the trend/slope to current popularity score 
        # based on the number month user entered
        # streamer[1] is the trend/slope of a streamer, streamer[2] is their current score
        prediction = num_month * streamer[1] + streamer[2]

        total_popularity = streamer[2]
        future_popularity_each_month = [total_popularity]

        # create a list of popualrity score for each month starting from the current month
        for i in range(0, num_month):
            total_popularity += streamer[1]
            future_popularity_each_month.append(total_popularity)
            
        predicted_popularity.append((streamer[0], prediction, future_popularity_each_month, streamer[1]))

    return predicted_popularity

