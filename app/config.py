import os
from dotenv import load_dotenv

load_dotenv()

SECREATE_KEY= os.getenv("SECREATE_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES"))
