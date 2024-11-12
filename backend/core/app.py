import os
from apiflask import APIFlask
from dotenv import load_dotenv
import google.generativeai as genai
from core.utils import instruction
import logging
import logging.config

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

'''Gemini AI Configuration'''
genai.configure(api_key=os.getenv('GEMINI_API'))
model = genai.GenerativeModel("models/gemini-1.5-flash",
                              system_instruction=instruction)
chat = model.start_chat()

'''Orders'''
orders = []

'''AI Status'''
'''Should be a dict or a list because bool are inmutable'''
ai_status = {'status': True}