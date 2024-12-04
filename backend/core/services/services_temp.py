import logging
import sys
import requests
import json
import time
import google.generativeai as genai
import os
from dotenv import load_dotenv
import threading
import re
from prompt import prompt
# from test_db import insert_order
# from test_vdb import rag
#process_messages
# import app

load_dotenv()

api = os.getenv('api_gemini')
genai.configure(api_key=api)

model = genai.GenerativeModel(
    "models/gemini-1.5-flash", 
)
def start_new_chat_session():
    return model.start_chat()

# def create_new_session(number):
#     session = {
#         'number': number,
#         'messages': [],  # Puedes almacenar los mensajes si es necesario
#         'state': 'new',  # Estado inicial
#         'timestamp': time.time()  # Marca de tiempo de la sesión
#     }
#     print(f"Sesión creada para el número {number}: {session}")
#     return session

#print(response.text)

recibos = []
class WhatsAppChatbot:
    def __init__(self, send_function, message_interval=5.0):
        self.send_function = send_function
        self.message_buffer = []
        self.timer = None
        self.lock = threading.Lock()
        self.message_interval = message_interval

    def receive_message(self, message, number, message_id, name, chat_session):
        with self.lock:
            self.message_buffer.append((message, number, message_id, name, chat_session))
            if self.timer is None:
                self.start_timer()

    def start_timer(self):
        self.timer = threading.Timer(self.message_interval, self.process_messages)
        self.timer.start()

    def process_messages(self):
        with self.lock:
            if not self.message_buffer:
                return

            '''
            number = '3244426751'
            combined_message_num_x = " ".join([msg[0] for msg in self.message_buffer if msg[1] == number])
            '''
            combined_message = " ".join([msg[0] for msg in self.message_buffer])

            '''
            messages_buffer = [
                0                        1           2       3            4
                ('Hola buenas noches', '3244426751', 1, 'Juan Diego', 'asdasd-sdasdads-dsasda'),
                ('Quisiera una hamburguesa', '3244426751', 2, 'Juan Diego', 'asdasd-sdasdads-dsasda'),
                ('Hola buenas noches', '3167461608', 3, 'Angela', 'sadasdsa-adsasdas-dasdsada')
            ]

            combined_message = """
                Hola buenas noches
                Quisiera una hamburguesa
                Hola buenas noches
            """
            '''


            number = self.message_buffer[0][1]
            message_id = self.message_buffer[0][2]
            name = self.message_buffer[0][3]
            chat_session = self.message_buffer[0][4]

            recibo_json = None
            try:
                content = rag(combined_message)
                context = prompt(content, combined_message)

                response = chat_session.send_message(context)
                response_text = response.text
                

                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    json_string = json_match.group(0)
                    json_string = json_string.replace(",]", "]").replace(",}", "}")

                    try:
                        recibo_json = json.loads(json_string)
                        
                        # print('JSON generado:', recibo_json)
                    
                    except json.JSONDecodeError as e:
                        logging.error(f"Error al decodificar JSON: {e}")
                        recibo_json = None

                    if recibo_json:
                        recibos.append(recibo_json)
                        print('recibo_json: ',recibo_json)
                        insert_order(recibo_json)
                        # print('Recibo almacenado en recibos:', recibos)
                        
                    response_text = response_text.replace(json_string, "").strip()
                else:
                    
                    print('No se encontró un JSON válido en la respuesta:', response_text)
            
            except Exception as e:
                logging.error(f"Error al procesar el mensaje: {e}")
                response_text = "Lo siento, no puedo procesar tu solicitud en este momento."
            finally:
                data = text_Message(number, response_text)
                self.send_function(data)

            self.message_buffer = []
            self.timer = None
            print("Finalizado el proceso de mensajes. Recibos actuales:", recibos)

    def obtener_recibos(self):
        with self.lock:
            # print('obt_recibos: ', recibos)
            return recibos


# Instancia de la clase

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = os.getenv('whatsapp_token')
        whatsapp_url = os.getenv('whatsapp_url')
        headers = {'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                headers=headers, 
                                data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data


def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def catalogo_Message(number):
    data = json.dumps(
        {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": number,
  "type": "interactive",
  "interactive": {
    "type": "catalog_message",
    "body": {
      "text": "Hello! Thanks for your interest. Ordering is easy. Just visit our catalog and add items to purchase."
    },
    "action": {
      "name": "catalog_message",
      "parameters": {
        "thumbnail_product_retailer_id": "2lc20305pt"
      }
    },
    "footer": {
      "text": "Best grocery deals on WhatsApp!"
            }
        }
        }
    )
    return data

def administrar_chatbot(textu, number, messageId, name, chat_session,chatbot):
    textu = textu.lower()
    print(f"Mensaje del usuario {number}: {textu}")
    chatbot.receive_message(textu, number, messageId, name, chat_session)

    # Marca el mensaje como leído
    markRead = markRead_Message(messageId)
    enviar_Mensaje_whatsapp(markRead)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s