import os
from dotenv import load_dotenv


load_dotenv()


IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV')
BOT_TOKEN = os.getenv('BOT_TOKEN')
