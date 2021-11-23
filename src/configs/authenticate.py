import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
TOKEN_TYPE = os.getenv("TOKEN_TYPE")
