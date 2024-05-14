from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "app" / "certs" / "jwt_private.perm"
    public_key_path: Path = BASE_DIR / "app" / "certs" / "jwt_public.perm"
    algorithm: str = "RS256"
    