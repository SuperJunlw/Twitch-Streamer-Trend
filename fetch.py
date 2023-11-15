import requests
import os
import time
from pprint import pprint as pp
from datetime import date

"""
    get the list of top 100 streamers in the past 7 days from StreamCharts 
    Client ID and Token needed
"""

def get_top_100_streamers():
    res = requests.get(' https://streamscharts.com/api/jazz/channels?platform=twitch&time=7-days', headers={
        "Client-ID": "Jfwu27gO2lFSwE6E",
        "Token": "$2y$10$m.jYZ6FNiPauWKFZAZPKeeFz0JVVVWY1UCMA39thMal8jmKPn52lu"
    })

    res = res.json()["data"]
    # pp(res)

    streamers = [None]*100
    for i, streamer in enumerate(res):
        streamers[i] = streamer["channel_name"]

    return streamers

"""
    Get the top #X+1 - #Y streamers' stats in the past 30 days from TwitchTracker
        ex. fetch_streamers_data(0, 100) = get the top #1 - #100 stats

    Please only fetch a few each time. API request won't work if you overburden the provider 
"""

def fetch_top_streamers_data(x,y):
    streamers_folder_dir = os.path.join(os.getcwd(), "streamers")
    if not os.path.isdir(streamers_folder_dir):
        os.makedirs(streamers_folder_dir)

    streamers = get_top_100_streamers()
    for streamer in streamers[x:y]:
        with open(os.path.join(streamers_folder_dir, f"{streamer}.txt"), "a") as f:
            f.write(str(date.today()) + ",")

            res = requests.get(f"https://twitchtracker.com/api/channels/summary/{streamer}")
            f.write(res.content.decode())
            f.write("\n")


# Code to fetch 5 streamers from the top 100 every 30 sec
# for i in range(20):
#     fetch_top_streamers_data(5*i, 5*(i+1))
#     time.sleep(30)


res = requests.get("https://twitchtracker.com/xcry/streams/49681755325")
print(res)