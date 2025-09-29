import jwt
from datetime import timedelta, datetime, timezone

from db.schemas.auth import TokenDataSchema

from config import HASH_ALGORITHM, JWT_SECRET_KEY, ACCESS_TOKEN_EXP


class AuthService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=float(ACCESS_TOKEN_EXP))):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=HASH_ALGORITHM)
        
        return encoded_jwt
    

    @staticmethod
    def get_user(token: str):        
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[HASH_ALGORITHM]) # type: ignore
        token_user_id = payload.get("sub")
        token_usrname = payload.get("username")
        
        token_data = TokenDataSchema(
            user_id=token_user_id
        )
        
        return token_data