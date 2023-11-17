import requests
import os
import time
from pprint import pprint as pp
from datetime import date

"""
    get the list of top 100 streamers (and their data) in the past 7 days from StreamCharts 
    Client ID and Token needed
"""

def get_top_100_streamers_data():
    res = requests.get(' https://streamscharts.com/api/jazz/channels?platform=twitch&time=7-days', headers={
        "Client-ID": "Jfwu27gO2lFSwE6E",
        "Token": "$2y$10$m.jYZ6FNiPauWKFZAZPKeeFz0JVVVWY1UCMA39thMal8jmKPn52lu"
    })

    # pp(res.json()["data"])
    return res.json()["data"]


"""
    store streamer's data to flat files. repeat for every streamer in the top 100 list
    data (including the list) is gathered from StreamChart
"""

def write_top_100_streamers_data():
    streamers_data = get_top_100_streamers_data()

    streamers_folder_dir = os.path.join(os.getcwd(), "streamers2")
    if not os.path.isdir(streamers_folder_dir):
        os.makedirs(streamers_folder_dir)
    
    extract = ['airtime_in_m', 'live_views', 'average_viewers', 'peak_viewers', 'hours_watched', 'followers_gain']
    
    for i, streamer in enumerate(streamers_data):
        with open(os.path.join(streamers_folder_dir, f"{streamer['channel_name']}.txt"), "a") as f:
            
            extract_dict = {"day": str(date.today()), "rank": i+1}
            for key in extract:
                extract_dict[key] = streamer[key]
            # extract_dict["followers_total"] = fetch_followers_total(streamer['channel_name'])

            f.write(str(extract_dict))
            f.write("\n")


"""
    Please only fetch a few each time. API request won't work if you overburden the provider 
"""

# def fetch_followers_total(streamer):
#     res = requests.get(f"https://twitchtracker.com/api/channels/summary/{streamer}")
#     time.sleep(6)
#     return res.json()["followers_total"]


# Call this code everyday
# write_top_100_streamers_data()
