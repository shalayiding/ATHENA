from dotenv import load_dotenv
import os

load_dotenv()
VERTEX_AI_API_KEY = os.getenv('VERTEX_AI_API_KEY')
MongoDB_uri = os.getenv('MongoDB_uri')
DC_BOT_TOKEN = os.getenv('DC_BOT_TOKEN')
VERTEX_AI_PROJECT_ID = os.getenv('VERTEX_AI_PROJECT_ID')