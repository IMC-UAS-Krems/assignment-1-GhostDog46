"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from .tracks import Track


class Artist:
    """
    Class representing a musician or content creator on the platform.

    Attributes:
        artist_id (str): Unique identifier for the artist.
        name (str): The name of the artist.
        genre (str): The primary genre associated with the artist.
        tracks (list[Track]): A list of tracks created by the artist.
    """

    def __init__(self, artist_id: str, name: str, genre: str, tracks: list[Track] = None):
        """
        Initialize a new Artist.

        Args:
            artist_id (str): Unique identifier.
            name (str): Artist's name.
            genre (str): Primary genre.
            tracks (list[Track], optional): Initial tracks. Defaults to None.
        """
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = tracks if tracks is not None else []

    def add_track(self, track: Track):
        """
        Associate a new track with the artist.

        Args:
            track (Track): The track to add.
        """
        self.tracks.append(track)

    def track_count(self) -> int:
        """
        Get the total number of tracks associated with the artist.

        Returns:
            int: Number of tracks.
        """
        return len(self.tracks)
