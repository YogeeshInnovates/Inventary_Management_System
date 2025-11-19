# import os
# from dotenv import load_dotenv

# load_dotenv()
# SECREATE_KEY= os.getenv("SECREATE_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES"))
# # DATABASE_URL = os.getenv("DATABASE_URL")

# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_USER = os.getenv("DB_USER")
# DB_PORT = os.getenv("DB_PORT")

# DB_NAME = os.getenv("DB_NAME")
# DB_HOST = os.getenv("DB_HOST")



# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


import os
from dotenv import load_dotenv

load_dotenv()

SECREATE_KEY = os.getenv("SECREATE_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES", 30))

# 1️⃣ PRIORITY: if CI test database URL exists → use it
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")
if DATABASE_URL_TEST:
    DATABASE_URL = DATABASE_URL_TEST

# 2️⃣ ELSE → use local DB configuration
else:
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_USER = os.getenv("DB_USER")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
