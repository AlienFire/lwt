from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.services.user_service import UserService
from app.db.models import User
from app.schema import Token, JWTData


class AuthorizationService:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    async def create_auth_token(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user = await self._find_user(username=form_data.username)
        self._verify_password(
            plain_password=form_data.password,
            hashed_password=user.password,
        )
        return await self._create_token(user=user)

    async def get_user_by_token(self, token: str) -> User:
        token_payload = self._decrypt_token(token)
        user = await self._user_service.get_by_id(id=token_payload.id)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User doesn't authorization",
            )
        return user

    async def _find_user(
        self,
        username: str,
    ) -> User:
        user = await self._user_service.find_user(username=username)
        if user is None:
            raise HTTPException(status_code=401, detail="Wrong username or password")
        return user

    def _verify_password(self, plain_password: str, hashed_password: str) -> None:
        if self._pwd_context.verify(plain_password, hashed_password):
            return None
        raise HTTPException(status_code=401, detail="Wrong username or password")

    async def _create_token(self, user: User) -> Token:
        data = JWTData(id=user.id, username=user.username)
        to_encode = data.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=encoded_jwt, token_type="bearer")

    def _decrypt_token(self, token: str) -> JWTData:
        try:
            raw_data = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="User doesn't authtorization",
            )
        return JWTData.model_validate(raw_data)
