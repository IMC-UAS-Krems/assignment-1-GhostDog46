"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .tracks import Track, Song
    from .users import FamilyAccountUser, PremiumUser, User, FamilyMember
    from .artists import Artist
    from .playlists import CollaborativePlaylist, Playlist
    from .sessions import ListeningSession
    from .albums import Album

from .tracks import Track, Song
from .users import FamilyAccountUser, PremiumUser, User, FamilyMember
from .artists import Artist
from .playlists import CollaborativePlaylist, Playlist
from .sessions import ListeningSession
from .albums import Album

class StreamingPlatform:
    def __init__(self, name: str, catalogue: dict[str, Track] = None, users: dict[str, User] = None, artists: dict[str, Artist] = None, albums: dict[str, Album] = None, playlists: dict[str, Playlist] = None, sessions: list[ListeningSession] = None):
        self.name = name
        self._catalogue = catalogue if catalogue is not None else {}
        self._users = users if users is not None else {}
        self._artists = artists if artists is not None else {}
        self._albums = albums if albums is not None else {}
        self._playlists = playlists if playlists is not None else {}
        self._sessions = sessions if sessions is not None else []

    def add_track(self, track: Track):
        self._catalogue[track.track_id] = track

    def add_user(self, user: User):
        self._users[user.user_id] = user
    
    def add_artist(self, artist: Artist):
        self._artists[artist.artist_id] = artist
    
    def add_album(self, album: Album):
        self._albums[album.album_id] = album
    
    def add_playlist(self, playlist: Playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession):
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str) -> Track | None:
        return self._catalogue.get(track_id)
    
    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)
    
    def get_artist(self, artist_id: str) -> Artist | None:
        return self._artists.get(artist_id)
    
    def get_album(self, album_id: str) -> Album | None:
        return self._albums.get(album_id)
    
    def all_users(self) -> list[User]:
        return list(self._users.values())
    
    def all_tracks(self) -> list[Track]:
        return list(self._catalogue.values())
    
    # Analytical queries

    def total_listening_time_minutes(self, start: datetime.datetime, end: datetime.datetime) -> float:
        total_seconds = 0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds
        return float(total_seconds / 60)

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        premium_users = [user for user in self._users.values() if type(user) is PremiumUser]
        
        if not premium_users:
            return 0.0
        
        total_unique_tracks = 0
        for user in premium_users:
            unique_tracks = set()
            for session in user.sessions:
                if session.timestamp >= cutoff:
                    unique_tracks.add(session.track.track_id)
            total_unique_tracks += len(unique_tracks)
        
        return float(total_unique_tracks / len(premium_users))
    
    def track_with_most_distinct_listeners(self) -> Track | None:
        if not self._sessions:
            return None
            
        track_listeners = {} 
        for session in self._sessions:
            if session.track.track_id not in track_listeners:
                track_listeners[session.track.track_id] = (session.track, set())
            track_listeners[session.track.track_id][1].add(session.user.user_id)
    
        if not track_listeners:
            return None
        
        best_track_id = max(track_listeners, key=lambda tid: len(track_listeners[tid][1]))
        return track_listeners[best_track_id][0]
    
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        user_types = ['FreeUser', 'PremiumUser', 'FamilyAccountUser', 'FamilyMember']
        type_durations = {ut: [] for ut in user_types}
        
        for session in self._sessions:
            utype = type(session.user).__name__
            if utype in type_durations:
                type_durations[utype].append(session.duration_listened_seconds)
        
        result = []
        for utype in user_types:
            durations = type_durations[utype]
            avg = float(sum(durations) / len(durations)) if durations else 0.0
            result.append((utype, avg))
            
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total_seconds = 0
        for user in self._users.values():
            if isinstance(user, FamilyMember) and user.age < age_threshold:
                for session in user.sessions:
                    total_seconds += session.duration_listened_seconds
        return float(total_seconds / 60)
    
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        artist_seconds = {}
        for session in self._sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                artist_seconds[artist] = artist_seconds.get(artist, 0) + session.duration_listened_seconds
        
        artist_minutes = [(artist, float(secs / 60)) for artist, secs in artist_seconds.items()]
        artist_minutes.sort(key=lambda x: x[1], reverse=True)
        return artist_minutes[:n]
    
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
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
            
        top_genre = max(genre_seconds.items(), key=lambda x: x[1])
        percentage = float((top_genre[1] / total_seconds) * 100)
        return (top_genre[0], percentage)
    
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        result = []
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artists = {track.artist for track in playlist.tracks if isinstance(track, Song)}
                if len(artists) > threshold:
                    result.append(playlist)
        return result
    
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        counts = {"Playlist": 0, "CollaborativePlaylist": 0}
        totals = {"Playlist": 0, "CollaborativePlaylist": 0}
        
        for playlist in self._playlists.values():
            if type(playlist) is CollaborativePlaylist:
                ptype = "CollaborativePlaylist"
            elif type(playlist) is Playlist:
                ptype = "Playlist"
            else:
                continue
            
            counts[ptype] += 1
            totals[ptype] += len(playlist.tracks)
            
        return {
            "Playlist": float(totals["Playlist"] / counts["Playlist"]) if counts["Playlist"] > 0 else 0.0,
            "CollaborativePlaylist": float(totals["CollaborativePlaylist"] / counts["CollaborativePlaylist"]) if counts["CollaborativePlaylist"] > 0 else 0.0
        }
    
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        result = []
        for user in self._users.values():
            user_track_ids = {s.track.track_id for s in user.sessions}
            completed_albums = set()
            
            albums_to_check = set()
            for session in user.sessions:
                if hasattr(session.track, 'album') and session.track.album:
                    albums_to_check.add(session.track.album)
            
            for album in albums_to_check:
                if not album.tracks:
                    continue
                if all(t.track_id in user_track_ids for t in album.tracks):
                    completed_albums.add(album.title)
            
            if completed_albums:
                result.append((user, sorted(list(completed_albums))))
        return result
