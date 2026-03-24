"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from .tracks import Track

class Artist:
    def __init__(self, artist_id: str, name: str, genre: str, tracks: list[Track] = None):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = tracks if tracks is not None else []
    
    def add_track(self, track):
        self.tracks.append(track)
    
    def track_count(self):
        return len(self.tracks)