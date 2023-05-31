import datetime
import json
import random
import re
import string
import urllib
from pprint import pprint

import requests
from googleapiclient.discovery import build
from rest_framework import status

from shared_music_play.settings import YOUTUBE_DATA_API_KEY
from web.models import Room


class Track:
    def __init__(self, title: str, track_url: str, thumbnail_url: str, duration: str = None):
        self.title = title
        self.track_url = track_url
        self.thumbnail_url = thumbnail_url
        self.duration = duration


def create_room_code(length=5) -> str:
    def get_code():
        return "".join(random.choice(string.ascii_uppercase) for i in range(length))

    code = get_code()
    while Room.objects.filter(code=code).exists():
        code = get_code()
    return code


def get_track_data_by_url(track_url) -> dict | None:
    if not track_url:
        return None
    youtube_re = (
        r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:["
        r"\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
    )
    if not re.fullmatch(youtube_re, track_url):
        return None

    params = {"format": "json", "url": track_url}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    if requests.get(url).status_code != status.HTTP_200_OK:
        return None

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return data


def get_videos_durations(youtube, videos_id):
    request = youtube.videos().list(part="contentDetails", id=",".join(videos_id))
    response = request.execute()
    if not response.get("items", None):
        return []
    json_data = response

    durations = []

    for item in json_data["items"]:
        duration_str = item["contentDetails"]["duration"]

        if re.match(r"^P(?:\d+D)?T(?:\d+H)?(?:\d+M)?\d+S$", duration_str):
            duration_parts = re.findall(r"\d+", duration_str)
            hours, minutes, seconds = 0, 0, 0
            if len(duration_parts) == 3:
                hours, minutes, seconds = map(int, duration_parts)
            elif len(duration_parts) == 2:
                minutes, seconds = map(int, duration_parts)
            elif len(duration_parts) == 1:
                seconds = int(duration_parts[0])
            duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        else:
            duration = datetime.timedelta(seconds=int(duration_str[2:-1]))

        hours = duration.seconds // 3600
        minutes = duration.seconds // 60 % 60
        seconds = duration.seconds % 60

        result = f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"

        durations.append(result)

    return durations


def get_list_track_by_search(search_query: str):
    if not search_query:
        return []

    youtube = build("youtube", "v3", developerKey=YOUTUBE_DATA_API_KEY)

    request = youtube.search().list(q=search_query, type="video", part="snippet", maxResults=15)
    response = request.execute()
    if not response.get("items", None):
        return []

    json_data = response

    track_list = []
    videos_ids = []
    for item in json_data["items"]:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            videos_ids.append(video_id)
            track_url = f"https://www.youtube.com/watch?v={video_id}"
            title = item["snippet"]["title"]
            thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]
            track = Track(title, track_url, thumbnail_url)
            track_list.append(track)

    durations = get_videos_durations(youtube, videos_ids)

    for duration, track in zip(durations, track_list):
        track.duration = duration

    return track_list
