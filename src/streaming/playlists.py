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
    def __init__(self, playlist_id: str, name: str, owner: User, tracks: list[Track] = None):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks if tracks is not None else []

    def add_track(self, track: Track):
        if track.track_id not in [t.track_id for t in self.tracks]:
            self.tracks.append(track)
            
    def remove_track(self, track_id: str):
        self.tracks = [t for t in self.tracks if t.track_id != track_id]
    
    def total_duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner, tracks: list[Track] = None, contributors: list[User] = None):
        super().__init__(playlist_id, name, owner, tracks)
        if contributors is not None:
            self.contributors = contributors
        else:
            self.contributors = [owner]

    def add_contributor(self, user: User):
        if user not in self.contributors:
            self.contributors.append(user)
            
    def remove_contributor(self, user: User):
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)
