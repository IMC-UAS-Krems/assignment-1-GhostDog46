"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""

import datetime
from .users import User
from .tracks import Track


class ListeningSession:
    """
    Class representing a single listening event where a user listens to a track.

    Attributes:
        session_id (str): Unique identifier for the session.
        user (User): The user who listened.
        track (Track): The track that was played.
        timestamp (datetime.datetime): When the session occurred.
        duration_listened_seconds (int): How long the user listened in seconds.
    """

    def __init__(self, session_id: str, user: User, track: Track, timestamp: datetime.datetime, duration_seconds: int):
        """
        Initialize a new ListeningSession.

        Args:
            session_id (str): Unique identifier.
            user (User): The user who listened.
            track (Track): The track that was played.
            timestamp (datetime.datetime): When the session occurred.
            duration_seconds (int): How long the user listened in seconds.
        """
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_seconds

    def duration_listened_minutes(self) -> float:
        """
        Calculate the duration listened in minutes.

        Returns:
            float: Duration in minutes.
        """
        return self.duration_listened_seconds / 60
