import ast
import os
from datetime import date, datetime

# Get and return the current stat of a streamer file
def read_file(filename):
    filepath = os.path.join("streamers2", filename)

    with open(filepath, 'r') as file:
        contents = file.read()

    contents = contents.split('\n')
    latest = ast.literal_eval(contents[-2]) # get the lastest data of a streamer

    return latest


# Return a list of file names of the current top 10 streamer
def get_current_top10_streamers():
    files = os.listdir('streamers2') # Get all files from the streamer2 folder

    top10 = []

    for i in range(10):

        lastest_file = None
        
        for file in files:
            current_stat = read_file(file)

            # Get the date of the lastest data of a streamer
            lastest_day = date(2000, 1, 1)
            current_date = datetime.strptime(current_stat['day'], "%Y-%m-%d").date()

            if current_stat['rank'] == i+1: # if the rank of the streamer is correct within the top 10
                if current_date > lastest_day: # if two streamer have same rank but different date, chose the lastest date
                    lastest_file = file

        top10.append(lastest_file)

    return top10


# Return a list of top 10 streamers' names
def get_streamer_names():
    top10 = get_top10_popularity()

    top10_names = ['All']

    for streamer in top10:
        top10_names.append(streamer[0])

    return top10_names


# Return a list of tuple of top 10 streamers, the tuple contain the steamer's name and popularity score
def get_top10_popularity():
    top10 = get_current_top10_streamers() # Get top 10 stremaer's files

    top10_popularity = []
    min_max = get_normal_min_max()

    for file in top10:
        stat = read_file(file)

        # Create tuple with file name and popularity score
        popularity = (file[:-4], compute_popularity(stat, min_max))

        top10_popularity.append(popularity)

    return top10_popularity


# Return a tuple with the min and max value of all the data use to compute the popularity score
def get_normal_min_max():
    top10 = get_current_top10_streamers()
    all_value = []

    for file in top10:
        stat = read_file(file)

        all_value.append(stat['average_viewers'])
        all_value.append(stat['peak_viewers'])
        all_value.append(stat['hours_watched'])
        all_value.append(stat['followers_gain'])

    return (min(all_value), max(all_value))


# Compute and return the popularity score of a streamer
def compute_popularity(stat, min_max):
    value1 = stat['average_viewers']
    value2 = stat['peak_viewers']
    value3 = stat['hours_watched']
    value4 = stat['followers_gain']

    # Normalized each value that will be used to compute the popularity
    # to ensure each value has equal representive in the score
    normalized_value1 = (value1 - min_max[0]) / (min_max[1] - min_max[0])
    normalized_value2 = (value2 - min_max[0]) / (min_max[1] - min_max[0])
    normalized_value3 = (value3 - min_max[0]) / (min_max[1] - min_max[0])
    normalized_value4 = (value4 - min_max[0]) / (min_max[1] - min_max[0])

    # Compute an overall value
    overall_value = (normalized_value1 + normalized_value2 + normalized_value3 + normalized_value4) / 4

    return overall_value


# Return a list that contains all prevous data of a streamer
def get_streamer_history(name):
    s_name = name + '.txt'
    filepath = os.path.join('streamers2', s_name)

    with open(filepath, 'r') as file:
        contents = file.read()

    contents = contents.split('\n')[:-1]

    evaulated_contents = []

    # Get each line of a streamer's file
    for line in contents:
        evaulated_line = ast.literal_eval(line)
        evaulated_contents.append(evaulated_line)

    return evaulated_contents
