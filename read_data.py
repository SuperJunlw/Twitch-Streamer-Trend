import ast
import os

# Get and return the current stat of a streamer file
def read_file(filename):
    filepath = os.path.join("streamers2", filename)

    with open(filepath, 'r') as file:
        contents = file.read()

    contents = contents.split('\n')
    latest = ast.literal_eval(contents[-2])

    return latest


def get_current_top10_streamers():
    files = os.listdir('streamers2')

    top10 = []

    for i in range(10):
        for file in files:
            current_stat = read_file(file)

            if current_stat['rank'] == i+1:
                top10.append(file)
                break

    return top10

def get_top10_popularity():
    top10 = get_current_top10_streamers()

    top10_popularity = []
    # extreme_stats = get_extremes_of_top10()

    for file in top10:
        stat = read_file(file)

        popularity = (file[:-4], compute_popularity(stat))
        # popularity = (file[:-4], compute_popularity(stat, extreme_stats))

        top10_popularity.append(popularity)

    return top10_popularity


def compute_popularity(stat):
    value1 = stat['average_viewers']
    value2 = stat['peak_viewers']
    value3 = stat['hours_watched']
    value4 = stat['followers_gain']

    normalized_value1 = (value1 - min(value1, value2, value3, value4)) / (max(value1, value2, value3, value4) - min(value1, value2, value3, value4))
    normalized_value2 = (value2 - min(value1, value2, value3, value4)) / (max(value1, value2, value3, value4) - min(value1, value2, value3, value4))
    normalized_value3 = (value3 - min(value1, value2, value3, value4)) / (max(value1, value2, value3, value4) - min(value1, value2, value3, value4))
    normalized_value4 = (value4 - min(value1, value2, value3, value4)) / (max(value1, value2, value3, value4) - min(value1, value2, value3, value4))

    # Compute an overall value
    overall_value = (normalized_value1 + normalized_value2 + normalized_value3 + normalized_value4) / 4

    return overall_value

print(get_top10_popularity())


# Slightly different approach to calculate popularity scores
# Make sure to uncomment get_top10_popularity() as well

# def get_extremes_of_top10():
#     top10 = get_current_top10_streamers()

#     average_viewers = []
#     peak_viewers    = []
#     hours_watched   = []
#     followers_gain  = []

#     for file in top10:
#         stat = read_file(file)

#         average_viewers.append(stat['average_viewers'])
#         peak_viewers.append(stat['peak_viewers'])
#         hours_watched.append(stat['hours_watched'])
#         followers_gain.append(stat['followers_gain'])

#     return [min(average_viewers), max(average_viewers), min(peak_viewers), max(peak_viewers), min(hours_watched), max(hours_watched), min(followers_gain), max(followers_gain)]


# def compute_popularity(stat, extreme_stats):
#     value1 = stat['average_viewers']
#     value2 = stat['peak_viewers']
#     value3 = stat['hours_watched']
#     value4 = stat['followers_gain']

#     normalized_value1 = (value1 - extreme_stats[0]) / (extreme_stats[1] - extreme_stats[0])
#     normalized_value2 = (value2 - extreme_stats[2]) / (extreme_stats[3] - extreme_stats[2])
#     normalized_value3 = (value3 - extreme_stats[4]) / (extreme_stats[5] - extreme_stats[4])
#     normalized_value4 = (value4 - extreme_stats[6]) / (extreme_stats[7] - extreme_stats[6])

#     # Compute an overall value
#     overall_value = (normalized_value1 + normalized_value2 + normalized_value3 + normalized_value4) / 4

#     return overall_value

# print(get_top10_popularity())