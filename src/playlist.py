import os
from googleapiclient.discovery import build
import datetime
import isodate

api_key = os.environ.get('API_KEY')


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self._fetch_data()

    def _fetch_data(self):
        youtube_service = build('youtube', 'v3', developerKey=api_key)

        response = youtube_service.playlists().list(
            part='snippet',
            id=self.playlist_id
        ).execute()

        if 'items' in response and response['items']:
            playlist_data = response['items'][0]['snippet']
            self.title = playlist_data['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        youtube_service = build('youtube', 'v3', developerKey=api_key)

        playlist_videos = youtube_service.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube_service.videos().list(
            part='contentDetails',
            id=','.join(video_ids)
        ).execute()

        total_duration = datetime.timedelta()

        for video in video_response['items']:
            iso_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        youtube_service = build('youtube', 'v3', developerKey=api_key)

        playlist_videos = youtube_service.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube_service.videos().list(
            part='statistics',
            id=','.join(video_ids)
        ).execute()

        best_video_id = max(video_response['items'], key=lambda x: int(x['statistics']['likeCount']))['id']

        return f"https://youtu.be/{best_video_id}"