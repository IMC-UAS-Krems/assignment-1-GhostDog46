"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""

from .artists import Artist
from .tracks import AlbumTrack


class Album:
    """
    Class representing a music album containing multiple tracks.

    Attributes:
        album_id (str): Unique identifier for the album.
        title (str): Title of the album.
        artist (Artist): The artist who created the album.
        release_year (int): The year the album was released.
        tracks (list[AlbumTrack]): The list of tracks in the album.
    """

    def __init__(self, album_id: str, title: str, artist: Artist, release_year: int, tracks: list[AlbumTrack] = None):
        """
        Initialize a new Album.

        Args:
            album_id (str): Unique identifier.
            title (str): Album title.
            artist (Artist): The creator.
            release_year (int): Release year.
            tracks (list[AlbumTrack], optional): Initial tracks. Defaults to None.
        """
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = tracks if tracks is not None else []

    def add_track(self, track: AlbumTrack):
        """
        Add a track to the album and maintain track order.

        Args:
            track (AlbumTrack): The track to add.
        """
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda t: t.track_number if t.track_number is not None else 0)

    def track_ids(self) -> set[str]:
        """
        Get the set of all track IDs in this album.

        Returns:
            set[str]: A set of track IDs.
        """
        return {track.track_id for track in self.tracks}

    def duration_seconds(self) -> int:
        """
        Calculate the total duration of the album in seconds.

        Returns:
            int: Total duration in seconds.
        """
        return sum(track.duration_seconds for track in self.tracks)
