import json

from googleapiclient.discovery import build

# Ключ API для работы с ютуб
api_key = 'AIzaSyAEaqHuKuD9q5oK4faLZ0BBvwW8RE_Dn08'

class Channel:
    """Класс для ютуб-канала"""
    def __init__(self, channel_id: str,) -> None:
        """Инициализирует id канала."""
        self.channel_id = channel_id
        self.title = None
        self.video_count = None
        self.url = None

        self._fetch_data()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f"Название канала: {self.title}")
        print(f"Количество видео: {self.video_count}")
        print(f"Ссылка на канал: {self.url}")

    @classmethod
    def get_service(cls):
        """Получает объект сервиса YouTube API."""
        youtube_service = build('youtube', 'v3', developerKey=api_key)
        return youtube_service

    def to_json(self, filename: str):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате JSON."""
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'url': self.url,
            'video_count': self.video_count,
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def _fetch_data(self):
        """Получает данные о канале через YouTube API."""
        youtube_service = self.get_service()

        # Запрос на получение данных о канале
        response = youtube_service.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()

        # Извлечение данных из ответа API и сохранение в атрибутах экземпляра
        channel = response['items'][0]
        self.title = channel['snippet']['title']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.video_count = channel['statistics']['videoCount']