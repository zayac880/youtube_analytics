import os
import json

from googleapiclient.discovery import build

# Ключ API для работы с ютуб
api_key = os.environ.get('API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    def __init__(self, channel_id: str,) -> None:
        """Инициализирует id канала."""
        self.channel_id = channel_id
        self.title = None
        self.description = None
        self.video_count = None
        self.subscriber_count = None
        self.view_count = None
        self.url = None

        self._fetch_data()

    def __str__(self):
        """Метод для отображения информации"""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Метод для операции сложения"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Метод для операции вычитания"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        """Метод для операции сравнения «меньше»"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Метод для операции сравнения «меньше или равно»"""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        """Метод для операции сравнения «больше»"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Метод для операции сравнения «больше или равно»"""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f"Название канала: {self.title}")
        print(f"Описание канала: {self.description}")
        print(f"Количество видео: {self.video_count}")
        print(f"Количество подписчиков: {self.subscriber_count}")
        print(f"Количество просмотров: {self.view_count}")
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
            'description': self.description,
            'url': self.url,
            'video_count': self.video_count,
            'subscriber_count': self.subscriber_count,
            'view_count': self.view_count,
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
        self.description = channel['snippet']['description']
        self.subscriber_count = channel['statistics']['subscriberCount']
        self.video_count = channel['statistics']['videoCount']
        self.view_count = channel['statistics']['viewCount']
