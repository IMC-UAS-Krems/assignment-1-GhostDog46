"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""

from abc import ABC, abstractmethod

class Track(ABC):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self):
        return self.duration_seconds / 60
    
    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds, genre, host, description=""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator

class AlbumTrack(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, album=None, track_number: int = None):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.album = album
        self.track_number = track_number

class SingleRelease(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date=None):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class InterviewEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, guest, description=""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest

class NarrativeEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, season: int, episode_number: int, description=""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number
