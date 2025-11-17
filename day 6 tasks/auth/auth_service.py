from db.memory_db import fake_users_db, blacklisted_tokens
from models.user_model import User
from core.security import hash_password, verify_password
from core.jwt_utils import create_access_token

class AuthService:

    @staticmethod
    def register(username: str, password: str, role: str):
        if username in fake_users_db:
            return None

        user = User(
            username=username,
            hashed_password=hash_password(password),
            role=role
        )

        fake_users_db[username] = user
        return user

    @staticmethod
    def authenticate(username: str, password: str):
        user = fake_users_db.get(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def generate_token(username: str, role: str):
        return create_access_token({"sub": username, "role": role})

    @staticmethod
    def logout(token: str):
        blacklisted_tokens.add(token)
