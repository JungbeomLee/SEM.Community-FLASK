# environment variable set

from dotenv import load_dotenv
import os

load_dotenv('../env')

database_pwd = os.environ.get("DAKTEABYASE")
jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
jwt_access_token_expires = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES"))
jwt_refresh_token_expires = int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES"))
