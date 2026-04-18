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

from abc import ABC


class Track(ABC):
    """
    Abstract base class representing a generic track on the platform.

    Attributes:
        track_id (str): Unique identifier for the track.
        title (str): Title of the track.
        duration_seconds (int): Duration of the track in seconds.
        genre (str): Genre classification for the track.
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        """
        Initialize a new Track.

        Args:
            track_id (str): Unique identifier for the track.
            title (str): Title of the track.
            duration_seconds (int): Duration of the track in seconds.
            genre (str): Genre classification for the track.
        """
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        """
        Calculate the track duration in minutes.

        Returns:
            float: The duration in minutes.
        """
        return self.duration_seconds / 60

    def __eq__(self, other) -> bool:
        """
        Compare two tracks for equality based on their track_id.

        Args:
            other (Any): The object to compare with.

        Returns:
            bool: True if both are Tracks and have the same track_id, False otherwise.
        """
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id


class Song(Track):
    """
    Class representing a music track associated with an artist.

    Attributes:
        artist (Artist): The artist who created the song.
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist):
        """
        Initialize a new Song.

        Args:
            track_id (str): Unique identifier for the song.
            title (str): Title of the song.
            duration_seconds (int): Duration of the song in seconds.
            genre (str): Genre classification for the song.
            artist (Artist): The artist who created the song.
        """
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist


class Podcast(Track):
    """
    Class representing a podcast episode.

    Attributes:
        host (str): The primary host of the podcast.
        description (str): A brief description of the episode content.
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, description: str = ""):
        """
        Initialize a new Podcast episode.

        Args:
            track_id (str): Unique identifier for the podcast episode.
            title (str): Title of the episode.
            duration_seconds (int): Duration of the episode in seconds.
            genre (str): Genre classification for the podcast.
            host (str): The primary host of the podcast.
            description (str, optional): A brief description. Defaults to "".
        """
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description


class AudiobookTrack(Track):
    """
    Class representing a chapter or segment of an audiobook.

    Attributes:
        author (str): The author of the audiobook.
        narrator (str): The narrator who read the audiobook.
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, author: str, narrator: str):
        """
        Initialize a new AudiobookTrack.

        Args:
            track_id (str): Unique identifier for the track.
            title (str): Title of the audiobook chapter.
            duration_seconds (int): Duration of the track in seconds.
            genre (str): Genre classification.
            author (str): The author of the audiobook.
            narrator (str): The narrator.
        """
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator


class AlbumTrack(Song):
    """
    Class representing a song that is part of an album.

    Attributes:
        album (Album, optional): The album this song belongs to.
        track_number (int, optional): The position of the song within the album.
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist, album=None, track_number: int = None):
        """
        Initialize a new AlbumTrack.

        Args:
            track_id (str): Unique identifier.
            title (str): Title of the song.
            duration_seconds (int): Duration in seconds.
            genre (str): Genre classification.
            artist (Artist): The artist.
            album (Album, optional): The album it belongs to. Defaults to None.
            track_number (int, optional): The track number on the album. Defaults to None.
        """
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.album = album
        self.track_number = track_number


class SingleRelease(Song):
    """
    Class representing a song released as a standalone single.

    Attributes:
        release_date (datetime.date, optional): The date the single was released.
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist, release_date=None):
        """
        Initialize a new SingleRelease.

        Args:
            track_id (str): Unique identifier.
            title (str): Title of the song.
            duration_seconds (int): Duration in seconds.
            genre (str): Genre classification.
            artist (Artist): The artist.
            release_date (datetime.date, optional): The release date. Defaults to None.
        """
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date


class InterviewEpisode(Podcast):
    """
    Class representing an interview-format podcast episode.

    Attributes:
        guest (str): The person being interviewed.
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, guest: str, description: str = ""):
        """
        Initialize a new InterviewEpisode.

        Args:
            track_id (str): Unique identifier.
            title (str): Title of the episode.
            duration_seconds (int): Duration in seconds.
            genre (str): Genre classification.
            host (str): The primary host.
            guest (str): The person being interviewed.
            description (str, optional): A brief description. Defaults to "".
        """
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest


class NarrativeEpisode(Podcast):
    """
    Class representing a narrative-format podcast episode.

    Attributes:
        season (int): The season number.
        episode_number (int): The episode number within the season.
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, season: int, episode_number: int, description: str = ""):
        """
        Initialize a new NarrativeEpisode.

        Args:
            track_id (str): Unique identifier.
            title (str): Title of the episode.
            duration_seconds (int): Duration in seconds.
            genre (str): Genre classification.
            host (str): The primary host.
            season (int): The season number.
            episode_number (int): The episode number.
            description (str, optional): A brief description. Defaults to "".
        """
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number
