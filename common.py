from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
import logging
from os import makedirs
from dotenv import load_dotenv

# ================= ENV =================
load_dotenv()

# ================= COLORS =================
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BLUE = "\033[94m"

# ================= LOGGER =================
class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        level_name = record.levelname
        if record.levelno == logging.DEBUG:
            return f"{BLUE}[{level_name}] {log_message}{RESET}"
        elif record.levelno == logging.INFO:
            return f"{GREEN}[{level_name}] {log_message}{RESET}"
        elif record.levelno == logging.WARNING:
            return f"{YELLOW}[{level_name}] {log_message}{RESET}"
        elif record.levelno >= logging.ERROR:
            return f"{RED}[{level_name}] {log_message}{RESET}"
        return f"[{level_name}] {log_message}"

makedirs("logs", exist_ok=True)

handler = logging.StreamHandler()
handler.setFormatter(
    ColorFormatter(
        "\nTime: %(asctime)s \nFile: %(filename)s:%(lineno)d \nMessage: %(message)s\n"
    )
)

file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter(
        "Time: %(asctime)s | Level: %(levelname)s | File: %(filename)s:%(lineno)d | Message: %(message)s\n"
    )
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(file_handler)

# ================= SETTINGS =================
class Settings(BaseSettings):
    DB_URL: str
    ASYNC_DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    NGROK_URL: str | None = None

    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: int | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()

# ================= AUTH =================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_expire = timedelta(days=1)
        self.refresh_expire = timedelta(days=30)

    # ---------- PASSWORD ----------
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        try:
            return pwd_context.verify(plain, hashed)
        except Exception:
            return plain == hashed

    # ---------- TOKEN ----------
    def _create_token(self, subject: str, expires_delta: timedelta, token_type: str):
        payload = {
        "sub": subject,
        "type": token_type,   # 🔥 MUHIM
        "exp": datetime.utcnow() + expires_delta,
    }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)


    def create_tokens(self, subject: str) -> dict:
        return {
        "accessToken": self._create_token(subject, self.access_expire, "access"),
        "refreshToken": self._create_token(subject, self.refresh_expire, "refresh"),
    }

    # ---------- DECODE ----------
    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

auth = AuthService()
