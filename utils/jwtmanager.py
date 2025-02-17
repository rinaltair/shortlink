from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import JWT, supported_key_types, AbstractJWKBase

from configs.settings import settings
from schemas.token import TokenData

# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = settings.JWT_SECRET_KEY
# ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
jwt = JWT()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class JWTManager():
    def __init__(self):
        # self.user_reps = UserRepositories(session)
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES


    async def key_instance(self) -> AbstractJWKBase:
        secret_bytes = self.secret_key.encode()
        return supported_key_types()['oct'](secret_bytes)


    async def create_access_token(self, data: dict, expires_delta: timedelta | None) -> str:
        """Create a new access token for a given data and expiration delta"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": int(expire.timestamp())})
        key =await self.key_instance()
        encode_jwt = jwt.encode(payload=to_encode, key= key, alg=self.algorithm)
        return encode_jwt


    async def verify_token(self, token: str) -> TokenData:
        """Verify the token and return the data"""
        payload = jwt.decode(token, key=await self.key_instance(), algorithms=self.algorithm)
        username: str = payload.get("sub")
        if username is None: raise Exception("Invalid token data")
        token_data = TokenData(username=username)
        return token_data

jwtmanager = JWTManager()
