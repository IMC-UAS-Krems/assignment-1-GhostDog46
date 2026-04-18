"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

import datetime
from .tracks import Track, Song
from .users import FamilyAccountUser, PremiumUser, User, FamilyMember
from .artists import Artist
from .playlists import CollaborativePlaylist, Playlist
from .sessions import ListeningSession
from .albums import Album


class StreamingPlatform:
    """
    The central orchestrator for the streaming platform.

    Manages users, tracks, artists, albums, and playlists, and provides 
    analytical tools to query platform data.

    Attributes:
        name (str): The name of the platform.
    """

    def __init__(self, name: str, catalogue: dict[str, Track] = None, users: dict[str, User] = None,
                 artists: dict[str, Artist] = None, albums: dict[str, Album] = None,
                 playlists: dict[str, Playlist] = None, sessions: list[ListeningSession] = None):
        """
        Initialize the StreamingPlatform.

        Args:
            name (str): Platform name.
            catalogue (dict[str, Track], optional): Track ID mapping. Defaults to None.
            users (dict[str, User], optional): User ID mapping. Defaults to None.
            artists (dict[str, Artist], optional): Artist ID mapping. Defaults to None.
            albums (dict[str, Album], optional): Album ID mapping. Defaults to None.
            playlists (dict[str, Playlist], optional): Playlist ID mapping. Defaults to None.
            sessions (list[ListeningSession], optional): All recorded sessions. Defaults to None.
        """
        self.name = name
        self._catalogue = catalogue if catalogue is not None else {}
        self._users = users if users is not None else {}
        self._artists = artists if artists is not None else {}
        self._albums = albums if albums is not None else {}
        self._playlists = playlists if playlists is not None else {}
        self._sessions = sessions if sessions is not None else []

    def add_track(self, track: Track):
        """Register a track in the catalogue."""
        self._catalogue[track.track_id] = track

    def add_user(self, user: User):
        """Register a user on the platform."""
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist):
        """Register an artist on the platform."""
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album):
        """Register an album on the platform."""
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist):
        """Register a playlist on the platform."""
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession):
        """Record a listening event and associate it with the user."""
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str) -> Track | None:
        """Retrieve a track by its ID."""
        return self._catalogue.get(track_id)

    def get_user(self, user_id: str) -> User | None:
        """Retrieve a user by their ID."""
        return self._users.get(user_id)

    def get_artist(self, artist_id: str) -> Artist | None:
        """Retrieve an artist by their ID."""
        return self._artists.get(artist_id)

    def get_album(self, album_id: str) -> Album | None:
        """Retrieve an album by its ID."""
        return self._albums.get(album_id)

    def all_users(self) -> list[User]:
        """Get a list of all registered users."""
        return list(self._users.values())

    def all_tracks(self) -> list[Track]:
        """Get a list of all registered tracks."""
        return list(self._catalogue.values())

    # Analytical queries

    def total_listening_time_minutes(self, start: datetime.datetime, end: datetime.datetime) -> float:
        """
        Calculate total listening time across all users within a time window.

        Args:
            start (datetime.datetime): Window start.
            end (datetime.datetime): Window end.

        Returns:
            float: Total time in minutes.
        """
        total_seconds = sum(
            s.duration_listened_seconds for s in self._sessions if start <= s.timestamp <= end
        )
        return float(total_seconds / 60)

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        """
        Calculate the average number of unique tracks listened to by PremiumUsers 
        in the last N days.

        Args:
            days (int, optional): The time window in days. Defaults to 30.

        Returns:
            float: The average count of unique tracks.
        """
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        premium_users = [user for user in self._users.values() if isinstance(user, PremiumUser)]

        if not premium_users:
            return 0.0

        total_unique_tracks = sum(
            len({s.track.track_id for s in u.sessions if s.timestamp >= cutoff})
            for u in premium_users
        )

        return float(total_unique_tracks / len(premium_users))

    def track_with_most_distinct_listeners(self) -> Track | None:
        """
        Identify the track that has been listened to by the highest number 
        of unique users.

        Returns:
            Track | None: The most popular track, or None if no sessions exist.
        """
        if not self._sessions:
            return None

        # Track mapping: track_id -> (Track object, set of unique user_ids)
        track_listeners = {}
        for session in self._sessions:
            tid = session.track.track_id
            if tid not in track_listeners:
                track_listeners[tid] = (session.track, set())
            track_listeners[tid][1].add(session.user.user_id)

        if not track_listeners:
            return None

        best_track_id = max(track_listeners, key=lambda tid: len(track_listeners[tid][1]))
        return track_listeners[best_track_id][0]

    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        """
        Calculate the average session duration (in seconds) for each user type.

        Returns:
            list[tuple[str, float]]: Sorted list of (UserType, AverageDuration) tuples.
        """
        user_types = ['FreeUser', 'PremiumUser', 'FamilyAccountUser', 'FamilyMember']
        type_durations = {ut: [] for ut in user_types}

        for session in self._sessions:
            utype = type(session.user).__name__
            if utype in type_durations:
                type_durations[utype].append(session.duration_listened_seconds)

        result = [
            (utype, float(sum(durations) / len(durations)) if durations else 0.0)
            for utype, durations in type_durations.items()
        ]

        # Sort by average duration descending
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        """
        Calculate total listening time for FamilyMembers under a certain age.

        Args:
            age_threshold (int, optional): The age limit. Defaults to 18.

        Returns:
            float: Total time in minutes.
        """
        total_seconds = sum(
            u.total_listening_seconds() 
            for u in self._users.values() 
            if isinstance(u, FamilyMember) and u.age < age_threshold
        )
        return float(total_seconds / 60)

    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        """
        Rank the top N artists based on cumulative listening time.

        Args:
            n (int, optional): Number of artists to return. Defaults to 5.

        Returns:
            list[tuple[Artist, float]]: List of (Artist, TotalMinutes) tuples.
        """
        artist_seconds = {}
        for session in self._sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                artist_seconds[artist] = artist_seconds.get(artist, 0) + session.duration_listened_seconds

        artist_minutes = [(artist, float(secs / 60)) for artist, secs in artist_seconds.items()]
        artist_minutes.sort(key=lambda x: x[1], reverse=True)
        return artist_minutes[:n]

    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        """
        Identify the most-listened-to genre for a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            tuple[str, float] | None: (GenreName, PercentageOfTotalTime) or None.
        """
        user = self.get_user(user_id)
        if not user or not user.sessions:
            return None

        genre_seconds = {}
        total_seconds = 0
        for session in user.sessions:
            genre = session.track.genre
            genre_seconds[genre] = genre_seconds.get(genre, 0) + session.duration_listened_seconds
            total_seconds += session.duration_listened_seconds

        if total_seconds == 0:
            return None

        top_genre_name, top_genre_secs = max(genre_seconds.items(), key=lambda x: x[1])
        percentage = float((top_genre_secs / total_seconds) * 100)
        return (top_genre_name, percentage)

    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        """
        Identify collaborative playlists that feature tracks from more than N distinct artists.

        Args:
            threshold (int, optional): The artist count threshold. Defaults to 3.

        Returns:
            list[CollaborativePlaylist]: A list of matching playlists.
        """
        result = [
            p for p in self._playlists.values()
            if isinstance(p, CollaborativePlaylist) and 
            len({t.artist for t in p.tracks if isinstance(t, Song)}) > threshold
        ]
        return result

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        """
        Compare the average number of tracks between standard and collaborative playlists.

        Returns:
            dict[str, float]: Mapping of playlist type names to average track counts.
        """
        metrics = {
            "Playlist": {"count": 0, "total_tracks": 0},
            "CollaborativePlaylist": {"count": 0, "total_tracks": 0}
        }

        for playlist in self._playlists.values():
            ptype = type(playlist).__name__
            if ptype in metrics:
                metrics[ptype]["count"] += 1
                metrics[ptype]["total_tracks"] += len(playlist.tracks)

        return {
            ptype: float(data["total_tracks"] / data["count"]) if data["count"] > 0 else 0.0
            for ptype, data in metrics.items()
        }

    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        """
        Identify users who have listened to every track in at least one album.

        Returns:
            list[tuple[User, list[str]]]: List of (User, list of AlbumTitles).
        """
        result = []
        for user in self._users.values():
            user_track_ids = user.unique_tracks_listened()
            completed_album_titles = []

            # Identify all albums the user has interacted with
            albums_interacted = {
                getattr(s.track, 'album') for s in user.sessions 
                if hasattr(s.track, 'album') and getattr(s.track, 'album')
            }

            # Check completion for each interacted album
            for album in albums_interacted:
                if album.tracks and all(t.track_id in user_track_ids for t in album.tracks):
                    completed_album_titles.append(album.title)

            if completed_album_titles:
                result.append((user, sorted(completed_album_titles)))
        
        return result
