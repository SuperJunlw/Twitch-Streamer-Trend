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

    for file in top10:
        stat = read_file(file)

        popularity = (file[:-4], compute_popularity(stat))

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




