import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


load_dotenv()
PROJECT_NAME = "ATRIS ADMIN CONSOLE"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_YEAR = int(os.getenv("REFRESH_TOKEN_EXPIRE_YEAR"))
EMAIL_TOKEN_EXPIRY_HOURS= int(os.getenv("EMAIL_TOKEN_EXPIRY_HOURS"))
CONF_URL = os.getenv("CONF_URL")
BACKEND_CORS_ORIGINS = [os.getenv("CORS_ORIGINS")] 
AUTH_REDIRECT_URL = os.getenv("AUTH_REDIRECT_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
DEFAULT_PROFILE_PIC = os.getenv("DEFAULT_PROFILE_PIC")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_TLS = True
MAIL_SSL = False
VERIFY_USER_URL = os.getenv("VERIFY_USER_URL")
FORGOT_PASSWORD_URL = os.getenv("FORGOT_PASSWORD_URL")
LOGIN_PAGE = os.getenv("LOGIN_PAGE")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login/")
MICRO_SERVICES_ACCESS_TOKEN = os.getenv("MICRO_SERVICES_ACCESS_TOKEN")
MICRO_SERVICES_ACCESS_TOKEN_EXP_YEARS = int(os.getenv("MICRO_SERVICES_ACCESS_TOKEN_EXP_YEARS"))
