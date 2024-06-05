from fastapi import Depends

from app.api.auth import AuthorizationService, oauth2_scheme, User
from app.di.services import get_user_service
from app.services import UserService


async def get_authorization_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthorizationService:
    return AuthorizationService(user_service=user_service)


async def get_auth_user(
    authorization: AuthorizationService = Depends(get_authorization_service),
    token: str = Depends(oauth2_scheme),
) -> User | None:
    return await authorization.get_user_by_token(token=token)
