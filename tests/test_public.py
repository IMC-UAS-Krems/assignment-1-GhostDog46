"""
test_public.py
--------------
Public test suite template.

This file provides a minimal framework and examples to guide you in writing
comprehensive tests for your StreamingPlatform implementation. Each test class
corresponds to one of the 10 query methods (Q1-Q10).

You should:
1. Study the examples provided
2. Complete the stub tests (marked with TODO or pass statements)
3. Add additional test cases for edge cases and boundary conditions
4. Verify your implementation passes all tests

Run with:
    pytest tests/test_public.py -v
"""

import pytest
from datetime import datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember, User
from streaming.playlists import CollaborativePlaylist, Playlist
from streaming.sessions import ListeningSession
from streaming.tracks import Song, SingleRelease
from streaming.artists import Artist
from tests.conftest import FIXED_NOW, RECENT, OLD


# ===========================================================================
# Q1 - Total cumulative listening time for a given period
# ===========================================================================

class TestTotalListeningTime:
    """Test the total_listening_time_minutes(start, end) method.
    
    This method should sum up all session durations that fall within
    the specified datetime window (inclusive on both ends).
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        start = RECENT - timedelta(hours=1)
        end = FIXED_NOW
        result = platform.total_listening_time_minutes(start, end)
        assert isinstance(result, float)

    def test_empty_window_returns_zero(self, platform: StreamingPlatform) -> None:
        """Test that a time window with no sessions returns 0.0."""
        far_future = FIXED_NOW + timedelta(days=365)
        result = platform.total_listening_time_minutes(
            far_future, far_future + timedelta(hours=1)
        )
        assert result == 0.0

    def test_known_period_value(self, platform: StreamingPlatform) -> None:
        u1 = platform.get_user("u1")
        t1 = platform.get_track("t1")
        s1 = ListeningSession("s1", u1, t1, RECENT, 180)
        platform.record_session(s1)

        start = RECENT - timedelta(seconds=1)
        end = RECENT + timedelta(seconds=1)
        assert platform.total_listening_time_minutes(start, end) == 3.0


# ===========================================================================
# Q2 - Average unique tracks per PremiumUser in the last N days
# ===========================================================================

class TestAvgUniqueTracksPremium:
    """Test the avg_unique_tracks_per_premium_user(days) method.
    
    This method should:
    - Count distinct tracks per PremiumUser in the last N days
    - Exclude FreeUser, FamilyAccountUser, and FamilyMember
    - Return 0.0 if there are no premium users
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        result = platform.avg_unique_tracks_per_premium_user(days=30)
        assert isinstance(result, float)

    def test_no_premium_users_returns_zero(self) -> None:
        """Test with a platform that has no premium users."""
        p = StreamingPlatform("EmptyPlatform")
        p.add_user(FreeUser("u99", "Nobody", age=25))
        assert p.avg_unique_tracks_per_premium_user() == 0.0

    def test_correct_value(self, platform: StreamingPlatform) -> None:
        bob = platform.get_user("u2")
        t1, t2 = platform.get_track("t1"), platform.get_track("t2")
        s1 = ListeningSession("s1", bob, t1, RECENT, 180)
        s2 = ListeningSession("s2", bob, t1, RECENT + timedelta(minutes=5), 180)
        s3 = ListeningSession("s3", bob, t2, RECENT + timedelta(minutes=10), 180)
        for s in (s1, s2, s3):
            platform.record_session(s)
        
        assert platform.avg_unique_tracks_per_premium_user(days=30) == 2.0


# ===========================================================================
# Q3 - Track with the most distinct listeners
# ===========================================================================

class TestTrackMostDistinctListeners:
    """Test the track_with_most_distinct_listeners() method.
    
    This method should:
    - Count the number of unique users who have listened to each track
    - Return the track with the highest count
    - Return None if the platform has no sessions
    """

    def test_empty_platform_returns_none(self) -> None:
        """Test that an empty platform returns None."""
        p = StreamingPlatform("Empty")
        assert p.track_with_most_distinct_listeners() is None

    def test_correct_track(self, platform: StreamingPlatform) -> None:
        u1, u2 = platform.get_user("u1"), platform.get_user("u2")
        t1, t2 = platform.get_track("t1"), platform.get_track("t2")
        
        s1 = ListeningSession("s1", u1, t1, RECENT, 180)
        platform.record_session(s1)
        
        s2 = ListeningSession("s2", u1, t2, RECENT, 180)
        s3 = ListeningSession("s3", u2, t2, RECENT, 180)
        for s in (s2, s3):
            platform.record_session(s)
        
        assert platform.track_with_most_distinct_listeners() == t2


# ===========================================================================
# Q4 - Average session duration per user subtype, ranked
# ===========================================================================

class TestAvgSessionDurationByType:
    """Test the avg_session_duration_by_user_type() method.
    
    This method should:
    - Calculate average session duration (in seconds) for each user type
    - Return a list of (type_name, average_duration) tuples
    - Sort results from longest to shortest duration
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (str, float) tuples."""
        result = platform.avg_session_duration_by_user_type()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], str) and isinstance(item[1], float)

    def test_sorted_descending(self, platform: StreamingPlatform) -> None:
        """Verify results are sorted by duration (longest first)."""
        result = platform.avg_session_duration_by_user_type()
        durations = [r[1] for r in result]
        assert durations == sorted(durations, reverse=True)

    def test_all_user_types_present(self, platform: StreamingPlatform) -> None:
        u1, u2 = platform.get_user("u1"), platform.get_user("u2")
        s1 = ListeningSession("s1", u1, platform.get_track("t1"), RECENT, 60)
        s2 = ListeningSession("s2", u2, platform.get_track("t1"), RECENT, 120)
        for s in (s1, s2):
            platform.record_session(s)
            
        result = platform.avg_session_duration_by_user_type()
        types = [r[0] for r in result]
        assert "FreeUser" in types
        assert "PremiumUser" in types
        free_avg = next(r[1] for r in result if r[0] == "FreeUser")
        assert free_avg == 60.0


# ===========================================================================
# Q5 - Total listening time for underage sub-users
# ===========================================================================

class TestUnderageSubUserListening:
    """Test the total_listening_time_underage_sub_users_minutes(age_threshold) method.
    
    This method should:
    - Count only sessions for FamilyMember users under the age threshold
    - Convert to minutes
    - Return 0.0 if no underage users or their sessions exist
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        result = platform.total_listening_time_underage_sub_users_minutes()
        assert isinstance(result, float)

    def test_no_family_users(self) -> None:
        """Test a platform with no family accounts."""
        p = StreamingPlatform("NoFamily")
        p.add_user(FreeUser("u1", "Solo", age=20))
        assert p.total_listening_time_underage_sub_users_minutes() == 0.0

    def test_correct_value_default_threshold(self, platform: StreamingPlatform) -> None:
        parent = FamilyAccountUser("parent", "Mom", 40)
        kid = FamilyMember("kid", "Junior", 12, parent)
        platform.add_user(parent)
        platform.add_user(kid)
        
        t1 = platform.get_track("t1")
        s1 = ListeningSession("s1", kid, t1, RECENT, 600)
        platform.record_session(s1)
        
        assert platform.total_listening_time_underage_sub_users_minutes() == 10.0

    def test_custom_threshold(self, platform: StreamingPlatform) -> None:
        parent = FamilyAccountUser("parent", "Dad", 45)
        teen = FamilyMember("teen", "Teenager", 16, parent)
        platform.add_user(parent)
        platform.add_user(teen)
        
        t1 = platform.get_track("t1")
        s1 = ListeningSession("s1", teen, t1, RECENT, 300)
        platform.record_session(s1)
        
        assert platform.total_listening_time_underage_sub_users_minutes(age_threshold=15) == 0.0
        assert platform.total_listening_time_underage_sub_users_minutes(age_threshold=18) == 5.0


# ===========================================================================
# Q6 - Top N artists by total listening time
# ===========================================================================

class TestTopArtistsByListeningTime:
    """Test the top_artists_by_listening_time(n) method.
    
    This method should:
    - Rank artists by total cumulative listening time (minutes)
    - Only count Song tracks (exclude Podcast and AudiobookTrack)
    - Return a list of (Artist, minutes) tuples
    - Sort from highest to lowest listening time
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (Artist, float) tuples."""
        from streaming.artists import Artist
        result = platform.top_artists_by_listening_time(n=3)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], Artist) and isinstance(item[1], float)

    def test_sorted_descending(self, platform: StreamingPlatform) -> None:
        """Verify results are sorted by listening time (highest first)."""
        result = platform.top_artists_by_listening_time(n=5)
        minutes = [r[1] for r in result]
        assert minutes == sorted(minutes, reverse=True)

    def test_respects_n_parameter(self, platform: StreamingPlatform) -> None:
        """Verify only the top N artists are returned."""
        result = platform.top_artists_by_listening_time(n=2)
        assert len(result) <= 2

    def test_top_artist(self, platform: StreamingPlatform) -> None:
        u1 = platform.get_user("u1")
        t1 = platform.get_track("t1")
        s1 = ListeningSession("s1", u1, t1, RECENT, 600)
        platform.record_session(s1)
        
        result = platform.top_artists_by_listening_time(n=1)
        assert len(result) == 1
        assert result[0][0].name == "Pixels"
        assert result[0][1] == 10.0


# ===========================================================================
# Q7 - User's top genre and percentage
# ===========================================================================

class TestUserTopGenre:
    """Test the user_top_genre(user_id) method.
    
    This method should:
    - Find the genre with the most listening time for a user
    - Return (genre_name, percentage_of_total_time)
    - Return None if user doesn't exist or has no sessions
    """

    def test_returns_tuple_or_none(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a tuple or None."""
        result = platform.user_top_genre("u1")
        if result is not None:
            assert isinstance(result, tuple) and len(result) == 2
            assert isinstance(result[0], str) and isinstance(result[1], float)

    def test_nonexistent_user_returns_none(self, platform: StreamingPlatform) -> None:
        """Test that a nonexistent user ID returns None."""
        assert platform.user_top_genre("does_not_exist") is None

    def test_percentage_in_valid_range(self, platform: StreamingPlatform) -> None:
        """Verify percentage is between 0 and 100."""
        for user in platform.all_users():
            result = platform.user_top_genre(user.user_id)
            if result is not None:
                _, pct = result
                assert 0.0 <= pct <= 100.0

    def test_correct_top_genre(self, platform: StreamingPlatform) -> None:
        u1 = platform.get_user("u1")
        t1 = platform.get_track("t1")
        t_jazz = SingleRelease("t_j1", "Jazz Song", 120, "jazz", platform.get_artist("a1"))
        platform.add_track(t_jazz)
        
        s1 = ListeningSession("s1", u1, t1, RECENT, 180)
        s2 = ListeningSession("s2", u1, t_jazz, RECENT, 120)
        for s in (s1, s2):
            platform.record_session(s)
            
        result = platform.user_top_genre("u1")
        assert result == ("pop", 60.0)


# ===========================================================================
# Q8 - CollaborativePlaylists with more than threshold distinct artists
# ===========================================================================

class TestCollaborativePlaylistsManyArtists:
    """Test the collaborative_playlists_with_many_artists(threshold) method.
    
    This method should:
    - Return all CollaborativePlaylist instances with >threshold distinct artists
    - Only count Song tracks (exclude Podcast and AudiobookTrack)
    - Return playlists in registration order
    """

    def test_returns_list_of_collaborative_playlists(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify the method returns a list of CollaborativePlaylist objects."""
        result = platform.collaborative_playlists_with_many_artists()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, CollaborativePlaylist)

    def test_higher_threshold_returns_empty(
        self, platform: StreamingPlatform
    ) -> None:
        """Test that a high threshold returns an empty list."""
        result = platform.collaborative_playlists_with_many_artists(threshold=100)
        assert result == []

    def test_default_threshold(self, platform: StreamingPlatform) -> None:
        u1 = platform.get_user("u1")
        cp = CollaborativePlaylist("cp1", "Multi-Artist Jam", owner=u1)
        for i in range(4):
            a = Artist(f"art_{i}", f"Artist {i}", "genre")
            platform.add_artist(a)
            t = Song(f"tr_{i}", f"Song {i}", 120, "genre", a)
            platform.add_track(t)
            cp.add_track(t)
        
        platform.add_playlist(cp)
        result = platform.collaborative_playlists_with_many_artists(threshold=3)
        assert cp in result
        
        result = platform.collaborative_playlists_with_many_artists(threshold=4)
        assert cp not in result


# ===========================================================================
# Q9 - Average tracks per playlist type
# ===========================================================================

class TestAvgTracksPerPlaylistType:
    """Test the avg_tracks_per_playlist_type() method.
    
    This method should:
    - Calculate average track count for standard Playlist instances
    - Calculate average track count for CollaborativePlaylist instances
    - Return a dict with keys "Playlist" and "CollaborativePlaylist"
    - Return 0.0 for types with no instances
    """

    def test_returns_dict_with_both_keys(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify the method returns a dict with both playlist types."""
        result = platform.avg_tracks_per_playlist_type()
        assert isinstance(result, dict)
        assert "Playlist" in result
        assert "CollaborativePlaylist" in result

    def test_standard_playlist_average(self, platform: StreamingPlatform) -> None:
        u1 = platform.get_user("u1")
        p1 = Playlist("p1", "My Favs", owner=u1)
        p1.add_track(platform.get_track("t1"))
        p1.add_track(platform.get_track("t2"))
        platform.add_playlist(p1)
        
        p2 = Playlist("p2", "Workout", owner=u1)
        p2.add_track(platform.get_track("t3"))
        platform.add_playlist(p2)
        
        result = platform.avg_tracks_per_playlist_type()
        assert result["Playlist"] == 1.5

    def test_collaborative_playlist_average(
        self, platform: StreamingPlatform
    ) -> None:
        u1 = platform.get_user("u1")
        cp = CollaborativePlaylist("cp1", "Group", owner=u1)
        cp.add_track(platform.get_track("t1"))
        cp.add_track(platform.get_track("t2"))
        cp.add_track(platform.get_track("t3"))
        platform.add_playlist(cp)
        
        result = platform.avg_tracks_per_playlist_type()
        assert result["CollaborativePlaylist"] == 3.0


# ===========================================================================
# Q10 - Users who completed at least one full album
# ===========================================================================

class TestUsersWhoCompletedAlbums:
    """Test the users_who_completed_albums() method.
    
    This method should:
    - Return users who have listened to every track on at least one album
    - Return (User, [album_titles]) tuples
    - Include all completed albums for each user
    - Ignore albums with no tracks
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (User, list) tuples."""
        from streaming.users import User
        result = platform.users_who_completed_albums()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], User) and isinstance(item[1], list)

    def test_completed_album_titles_are_strings(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify all completed album titles are strings."""
        result = platform.users_who_completed_albums()
        for _, titles in result:
            assert all(isinstance(t, str) for t in titles)

    def test_correct_users_identified(self, platform: StreamingPlatform) -> None:
        u1 = platform.get_user("u1")
        for i in (1, 2, 3):
            t = platform.get_track(f"t{i}")
            s = ListeningSession(f"s{i}", u1, t, RECENT, 180)
            platform.record_session(s)
            
        result = platform.users_who_completed_albums()
        users = [r[0] for r in result]
        assert u1 in users

    def test_correct_album_titles(self, platform: StreamingPlatform) -> None:
        u1 = platform.get_user("u1")
        for i in (1, 2, 3):
            t = platform.get_track(f"t{i}")
            s = ListeningSession(f"s{i}", u1, t, RECENT, 180)
            platform.record_session(s)
            
        result = platform.users_who_completed_albums()
        u1_albums = next(r[1] for r in result if r[0] == u1)
        assert "Digital Dreams" in u1_albums
