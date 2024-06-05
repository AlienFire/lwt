from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.di.services import get_user_service
from app.services.user_service import UserService

auth_router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class JWTData(BaseModel):
    id: int
    username: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db, username: str) -> UserInDB | None:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@auth_router.post("/token/")
async def auth_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(get_user_service),
) -> Token:
    user = await service.find_user(username=form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    data = JWTData(id=user.id, username=user.username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    assess_token = create_access_token(
        data=data.model_dump(),
        expires_delta=access_token_expires,
    )
    return Token(access_token=assess_token, token_type="bearer")


class AuthorizationService:
    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def get_user_by_token(self, token: str) -> User:
        # Decrypt and validate token
        # Find user by token data (id or name)
        token_payload = self._decrypt_token(token)
        user = await self._user_service.get_by_id(id=token_payload.id)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User doesn't authorization",
            )
        return user

    def _decrypt_token(self, token: str) -> JWTData:
        try:
            raw_data = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="User doesn't authtorization",
            )
        return JWTData.model_validate(raw_data)
