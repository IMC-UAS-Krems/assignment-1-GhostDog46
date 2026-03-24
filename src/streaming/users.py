"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

from abc import ABC

class User(ABC):
    def __init__(self, user_id: str, name: str, age: int, sessions=None):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = sessions if sessions is not None else []

    def add_session(self, session):
        self.sessions.append(session)
    
    def total_listening_seconds(self) -> int:
        return sum(session.duration_listened_seconds for session in self.sessions)
    
    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60
    
    def unique_tracks_listened(self) -> set[str]:
        return {session.track.track_id for session in self.sessions}

class FreeUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.MAX_SKIPS_PER_HOUR = 6

class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start=None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.sub_users = []
    
    def add_sub_user(self, sub_user):
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)
    
    def all_members(self):
        return [self] + self.sub_users

class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent
        parent.add_sub_user(self)
