# This module defines the Settings class, which loads configuration values from environment variables using the `dotenv` library. It includes settings for database connection, AWS S3 credentials, Redis URL, SendGrid API key, OpenAI API key, and JWT token settings. The `Settings` class provides a centralized place to manage all configuration values for the application, making it easier to maintain and secure sensitive information. The `settings` instance is created at the end of the module, allowing other parts of the application to access these configuration values easily.

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_REGION = os.getenv("AWS_REGION")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # JWT Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
    ALGORITHM = "HS256" # Yeh encryption ka tarika (Hashing Algorithm) hai. HS256 standard aur bohot secure algorithm hai jo token ko signature lagane ke liye use hota hai.
    ACCESS_TOKEN_EXPIRE_MINUTES = 30 # User ka main token sirf 30 minutes ke liye valid rahega. 30 mins baad yeh expiry ki wajah se bekaar ho jayega. Iska faida yeh hai ke agar koi aapka token chura bhi le, to wo 30 mins baad khud hi expire ho jayega.
    REFRESH_TOKEN_EXPIRE_DAYS = 7   # Refresh token 7 din ke liye valid rahega. Iska matlab hai ke user apne access token ko refresh kar sakta hai bina baar baar login kiye, lekin wo refresh token bhi 7 din baad expire ho jayega, jisse security badh jati hai.

settings = Settings()


