from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.errors import UnauthorizedError
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


async def get_chat_repo(session: AsyncSession = Depends(get_session)) -> ChatMessageRepository:
    return ChatMessageRepository(session)


def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()


async def get_auth_usecase(
    user_repo: UserRepository = Depends(get_user_repo),
) -> AuthUseCase:
    return AuthUseCase(user_repo)


async def get_chat_usecase(
    chat_repo: ChatMessageRepository = Depends(get_chat_repo),
    openrouter_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    return ChatUseCase(chat_repo, openrouter_client)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:
    try:
        payload = security.decode_token(token)
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise UnauthorizedError("Invalid token")
        return int(user_id_str)
    except (JWTError, ValueError, UnauthorizedError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e