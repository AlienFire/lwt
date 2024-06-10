from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db.models import User
from app.di.services import get_user_service
from app.schema import Token
from app.services import UserService
from app.services.auth_services import AuthorizationService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_authorization_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthorizationService:
    return AuthorizationService(user_service=user_service)


async def get_auth_user(
    authorization: AuthorizationService = Depends(get_authorization_service),
    token: str = Depends(oauth2_scheme),
) -> User | None:
    return await authorization.get_user_by_token(token=token)


async def get_auth_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authorization: AuthorizationService = Depends(get_authorization_service),
) -> Token:
    return await authorization.create_auth_token(form_data=form_data)
