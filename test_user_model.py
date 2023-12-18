"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_authenticate_user(self):
        """
        Authenticates a user with the given username and password.

        Args:
            none

        Returns:
            bool: True if the user was authenticated, False otherwise.

        Raises:
            ValueError: If the username or password is invalid.
        """

        hashed_pwd = bcrypt.generate_password_hash(
            "HASHED_PASSWORD").decode('utf-8')
        u = User(email="test@test.com",
                 username="test2user", password=hashed_pwd)

        db.session.add(u)
        db.session.commit()

        user = User.query.filter_by(username=u.username).first()

        self.assertTrue(user.authenticate("test2user", "HASHED_PASSWORD"))

    def test_authentication_fail(self):
        """Test authentication failure

        This function tests the authentication failure functionality in the User model. It creates a user, u2, and then tries to authenticate u2 with the wrong password. It then checks if u2 is authenticated, which should return False.

        Args:
            None

        Returns:
            True if u2 is authenticated, False otherwise

        Raises:
            AssertionError if the test fails
        """
        hashed_pwd = bcrypt.generate_password_hash(
            "HASHED_PASSWORD").decode('utf-8')
        u2 = User(email="test@test.com",
                  username="test2user", password=hashed_pwd)
        db.session.add(u2)
        db.session.commit()

        user = User.query.filter_by(username=u2.username).first()

        self.assertFalse(user.authenticate(
            "test2user", "WRONG_PASSWORD"))

    def test_user_is_following(self):
        """Test user following

        This function tests the user following functionality in the User model. It creates two users, u2 and u3, and then adds a follow relationship between them. It then checks if u2 is following u3, which should return True.

        Args:
            None

        Returns:
            True if u2 is following u3, False otherwise

        Raises:
            AssertionError if the test fails
        """
        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()

        u3 = User(
            email="test3@test.com",
            username="test3user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u3)
        db.session.commit()

        u2.following.append(u3)
        db.session.commit()
        self.assertTrue(u2.is_following(u3))

    def test_user_is_followed_by(self):
        """
        Test user following

        This function tests the user following functionality in the User model. It creates two users, u2 and u3, and then adds a follow relationship between them. It then checks if u2 is following u3, which should return True.

        Args:
            None

        Returns:
            True if u2 is following u3, False otherwise

        Raises:
            AssertionError if the test fails
        """
        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()

        u3 = User(
            email="test3@test.com",
            username="test3user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u3)
        db.session.commit()

        u3.following.append(u2)

        # this function returns true if u2 is following u3
        self.assertTrue(u2.is_followed_by(u3))
