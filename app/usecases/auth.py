from app.core import security
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.repositories.users import UserRepository
from app.schemas.user import UserPublic


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> UserPublic:
        existing = await self._user_repo.get_by_email(email)
        if existing:
            raise ConflictError("User with this email already exists")
        hashed = security.hash_password(password)
        user = await self._user_repo.create(email, hashed)
        return UserPublic.model_validate(user)

    async def login(self, email: str, password: str) -> str:
        user = await self._user_repo.get_by_email(email)
        if not user or not security.verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        token_data = {"sub": str(user.id), "role": user.role}
        token = security.create_access_token(token_data)
        return token

    async def get_profile(self, user_id: int) -> UserPublic:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return UserPublic.model_validate(user)