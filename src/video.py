import os
import json

from googleapiclient.discovery import build

# Ключ API для работы с ютуб
api_key = os.environ.get('API_KEY')


class Video:
    def __init__(self, video_id: str, ):
        """Инициализирует id видео."""
        self.video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None
        self._fetch_data()

    def __str__(self):
        """Метод для отображения информации"""
        return f'{self.title}'

    @classmethod
    def get_service(cls):
        """Получает объект сервиса YouTube API."""
        youtube_service = build('youtube', 'v3', developerKey=api_key)
        return youtube_service

    def _fetch_data(self):
        """Получает данные о канале через YouTube API."""
        youtube_service = self.get_service()

        # Запрос на получение данных о видео
        response = youtube_service.videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.video_id
        ).execute()

        # Извлечение данных из ответа API и сохранение в атрибутах экземпляра
        video_response = response['items'][0]
        self.title = video_response['snippet']['title']
        self.url = f"https://www.youtube.com/video/{self.video_id}"
        self.view_count = video_response['statistics']['viewCount']
        self.like_count = video_response['statistics']['likeCount']


class PLVideo(Video):
    def __init__(self, video_id, id_playlist):
        """Инициализирует id видео и id плейлиста"""
        super().__init__(video_id)
        self.id_playlist = id_playlist



