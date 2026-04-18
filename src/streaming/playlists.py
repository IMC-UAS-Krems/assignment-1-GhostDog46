"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

from .users import User
from .tracks import Track


class Playlist:
    """
    Class representing a user-curated collection of tracks.

    Attributes:
        playlist_id (str): Unique identifier for the playlist.
        name (str): Name of the playlist.
        owner (User): The user who created the playlist.
        tracks (list[Track]): The list of tracks in the playlist.
    """

    def __init__(self, playlist_id: str, name: str, owner: User, tracks: list[Track] = None):
        """
        Initialize a new Playlist.

        Args:
            playlist_id (str): Unique identifier.
            name (str): Playlist name.
            owner (User): The owner.
            tracks (list[Track], optional): Initial tracks. Defaults to None.
        """
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks if tracks is not None else []

    def add_track(self, track: Track):
        """
        Add a track to the playlist if it is not already present.

        Args:
            track (Track): The track to add.
        """
        if track.track_id not in [t.track_id for t in self.tracks]:
            self.tracks.append(track)

    def remove_track(self, track_id: str):
        """
        Remove a track from the playlist by its ID.

        Args:
            track_id (str): The ID of the track to remove.
        """
        self.tracks = [t for t in self.tracks if t.track_id != track_id]

    def total_duration_seconds(self) -> int:
        """
        Calculate the total duration of all tracks in the playlist.

        Returns:
            int: Total duration in seconds.
        """
        return sum(track.duration_seconds for track in self.tracks)


class CollaborativePlaylist(Playlist):
    """
    Class representing a playlist that multiple users can contribute to.

    Attributes:
        contributors (list[User]): List of users allowed to modify the playlist.
    """

    def __init__(self, playlist_id: str, name: str, owner: User, tracks: list[Track] = None, contributors: list[User] = None):
        """
        Initialize a new CollaborativePlaylist.

        Args:
            playlist_id (str): Unique identifier.
            name (str): Playlist name.
            owner (User): The owner.
            tracks (list[Track], optional): Initial tracks. Defaults to None.
            contributors (list[User], optional): Initial contributors. Defaults to None.
        """
        super().__init__(playlist_id, name, owner, tracks)
        if contributors is not None:
            self.contributors = contributors
        else:
            self.contributors = [owner]

    def add_contributor(self, user: User):
        """
        Grant a user permission to contribute to the playlist.

        Args:
            user (User): The user to add as a contributor.
        """
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user: User):
        """
        Revoke a user's permission to contribute, unless they are the owner.

        Args:
            user (User): The user to remove.
        """
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)
