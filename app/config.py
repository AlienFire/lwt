from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "app" / "certs" / "jwt_private.perm"
    public_key_path: Path = BASE_DIR / "app" / "certs" / "jwt_public.perm"
    # algorithm: str = "RS256"


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30