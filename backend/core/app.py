import os
import logging
import logging.config
from apiflask import APIFlask
from dotenv import load_dotenv
from core.services.create_vdb import update_vectoredb
import google.generativeai as genai
from sqlalchemy.orm import sessionmaker
from sqlalchemy import QueuePool, create_engine
from core.utils import instruction



load_dotenv()


'''Logger config'''
logging.config.fileConfig('log.conf')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')

app = APIFlask(__name__)

app.config['HOST'] = HOST = os.getenv('HOST') or 'localhost'
app.config['PORT'] = PORT = os.getenv('PORT') or '5000'
app.config['WHATSAPP_TOKEN'] = os.getenv('WHATSAPP_TOKEN')
app.config['WHATSAPP_URL'] = os.getenv('WHATSAPP_URL')
app.config['WEBHOOK_VERIFY_TOKEN'] = os.getenv('WEBHOOK_VERIFY_TOKEN')
DB_DIR = os.getenv('DB_DIR') # Chroma DB DIR
MODEL_NAME = app.config['MODEL_NAME'] = os.getenv('MODEL_NAME')
DB_URL = app.config['DB_URL'] = os.getenv('DB_URL') # Supabase URL
CURRENT_DIR = os.getcwd()


'''Supabase URL'''
engine = create_engine(DB_URL, poolclass=QueuePool, pool_size=5, max_overflow=10)
Session = sessionmaker(bind=engine)


'''Check DB_PATH exists'''
DB_PATH = app.config['DB_PATH'] = f'{CURRENT_DIR}/{DB_DIR}' # Chroma DB PATH
if not(os.path.isdir(DB_PATH)):
    os.mkdir(DB_PATH)
    update_vectoredb(DB_PATH, MODEL_NAME, Session)


'''Gemini AI Configuration'''
genai.configure(api_key=os.getenv('GEMINI_API'))
model = genai.GenerativeModel("models/gemini-1.5-flash",system_instruction=instruction)
# chat = model.start_chat()
#chat_sessions = {}


'''Orders'''
orders = []


'''AI Status'''
'''Should be a dict or a list because bool are inmutable'''
ai_status = {'status': True}


