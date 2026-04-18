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
from collections.abc import Sequence


class User(ABC):
    """
    Abstract base class representing a platform user.

    Attributes:
        user_id (str): Unique identifier for the user.
        name (str): Name of the user.
        age (int): Age of the user.
        sessions (list[ListeningSession]): List of listening sessions associated with the user.
    """

    def __init__(self, user_id: str, name: str, age: int, sessions=None):
        """
        Initialize a new User.

        Args:
            user_id (str): Unique identifier.
            name (str): User's name.
            age (int): User's age.
            sessions (list[ListeningSession], optional): Initial sessions. Defaults to None.
        """
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = sessions if sessions is not None else []

    def add_session(self, session):
        """
        Record a new listening session for the user.

        Args:
            session (ListeningSession): The session to add.
        """
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        """
        Calculate the total time the user has spent listening in seconds.

        Returns:
            int: Total duration in seconds.
        """
        return sum(session.duration_listened_seconds for session in self.sessions)

    def total_listening_minutes(self) -> float:
        """
        Calculate the total time the user has spent listening in minutes.

        Returns:
            float: Total duration in minutes.
        """
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self) -> set[str]:
        """
        Get the set of unique track IDs the user has listened to.

        Returns:
            set[str]: A set of unique track IDs.
        """
        return {session.track.track_id for session in self.sessions}


class FreeUser(User):
    """
    Class representing a user on the free tier.

    Attributes:
        MAX_SKIPS_PER_HOUR (int): Maximum number of skips allowed per hour.
    """

    def __init__(self, user_id: str, name: str, age: int):
        """
        Initialize a new FreeUser.

        Args:
            user_id (str): Unique identifier.
            name (str): User's name.
            age (int): User's age.
        """
        super().__init__(user_id, name, age)
        self.MAX_SKIPS_PER_HOUR = 6


class PremiumUser(User):
    """
    Class representing a premium subscriber.

    Attributes:
        subscription_start (datetime.datetime, optional): When the subscription started.
    """

    def __init__(self, user_id: str, name: str, age: int, subscription_start=None):
        """
        Initialize a new PremiumUser.

        Args:
            user_id (str): Unique identifier.
            name (str): User's name.
            age (int): User's age.
            subscription_start (datetime.datetime, optional): Subscription start date. Defaults to None.
        """
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(User):
    """
    Class representing a premium user managing a family account.

    Attributes:
        sub_users (list[FamilyMember]): List of family members under this account.
    """

    def __init__(self, user_id: str, name: str, age: int):
        """
        Initialize a new FamilyAccountUser.

        Args:
            user_id (str): Unique identifier.
            name (str): User's name.
            age (int): User's age.
        """
        super().__init__(user_id, name, age)
        self.sub_users = []

    def add_sub_user(self, sub_user):
        """
        Add a family member to the account.

        Args:
            sub_user (FamilyMember): The family member to add.
        """
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)

    def all_members(self) -> Sequence[User]:
        """
        Get all users associated with this family account (including the owner).

        Returns:
            Sequence[User]: A sequence containing the owner and all sub-users.
        """
        return [self] + self.sub_users


class FamilyMember(User):
    """
    Class representing a profile belonging to a family account.

    Attributes:
        parent (FamilyAccountUser): The owner of the family account.
    """

    def __init__(self, user_id: str, name: str, age: int, parent: FamilyAccountUser):
        """
        Initialize a new FamilyMember.

        Args:
            user_id (str): Unique identifier.
            name (str): User's name.
            age (int): User's age.
            parent (FamilyAccountUser): The account owner.
        """
        super().__init__(user_id, name, age)
        self.parent = parent
        parent.add_sub_user(self)
