from dotenv import load_dotenv
import os
import subprocess

def get_gcloud_access_token():
    try:
        access_token = subprocess.check_output(['gcloud', 'auth', 'print-access-token'], text=True).strip()
        return access_token
    except FileNotFoundError:
        print("Failed to obtain access token:")
        return None

VERTEX_AI_API_KEY = get_gcloud_access_token()


load_dotenv()
if VERTEX_AI_API_KEY ==None:
    VERTEX_AI_API_KEY = os.getenv('VERTEX_AI_API_KEY')

MongoDB_uri = os.getenv('MongoDB_uri')
DC_BOT_TOKEN = os.getenv('DC_BOT_TOKEN')
VERTEX_AI_PROJECT_ID = os.getenv('VERTEX_AI_PROJECT_ID')