import os
from dotenv import load_dotenv

load_dotenv()
SECREATE_KEY= os.getenv("SECREATE_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES"))
# DATABASE_URL = os.getenv("DATABASE_URL")

# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_USER = os.getenv("DB_USER")
# DB_PORT = os.getenv("DB_PORT")

# DB_NAME = os.getenv("DB_NAME")
# DB_HOST = os.getenv("DB_HOST")


# TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
# TEST_DB_USER  = os.getenv("TEST_DB_USER")
# TEST_DB_PORT  = os.getenv("TEST_DB_PORT")
# TEST_DB_NAME  = os.getenv("TEST_DB_NAME")
# TEST_DB_HOST  = os.getenv("TEST_DB_HOST")

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DATABASE_URL_TEST =  f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

DATABASE_URL=os.getenv("DATABASE_URL")
DATABASE_URL_TEST=os.getenv("DATABASE_URL_TEST")