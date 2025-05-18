import os

import dotenv

dotenv.load_dotenv()
TEPROLIN_API_HOST = os.getenv('TEPROLIN_API_HOST')
TEPROLIN_API_PORT = os.getenv('TEPROLIN_API_PORT')

TEPROLIN_API = 'http://' + TEPROLIN_API_HOST + ':' + TEPROLIN_API_PORT

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
