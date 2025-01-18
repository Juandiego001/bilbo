import json
import re
import requests
from datetime import datetime
from core.app import app, model, info_logger, error_logger, orders, ai_status
from core.services.rag import rag
from core.services.prompt import prompt
import threading

# Buffer global para almacenar mensajes por número
messages_buffer = {}
timers = {}  # Diccionario para manejar timers por número
chat_sessions = {}
lock = threading.Lock()

def get_or_create_chat_session(number):
    """Obtiene o crea una sesión de chat para un usuario específico."""
    global chat_sessions
    with lock:
        if number not in chat_sessions:
            chat_sessions[number] = model.start_chat()
        return chat_sessions[number]

def ai_process_message(number: str):
    '''Procesar y enviar mensajes acumulados'''
    global messages_buffer, timers

    if number not in messages_buffer:
        return

    combined_message = " ".join([msg for msg, _ in messages_buffer[number]])

    try:
        # Procesamiento de IA
        chat = get_or_create_chat_session(number)
        
        content = rag(combined_message)
        context = prompt(content, combined_message)
        chat.history.append({"role": "user", "parts": combined_message})
        
        # print('chat history ah',chat.history)
        #print('combined_message: ',combined_message)
        
        response_text = chat.send_message(context).text
        #print('aqui')
        chat.history.append({"role": "model", "parts": response_text})
        #print('chat: ', chat)
        # print('response_text: ',response_text)

        info_logger.info(f'Response text: {response_text}')

        if '`' in response_text:
            response_text = response_text.replace('```', '')
            response_text = response_text.replace('json', '')

        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            json_string = json_string.replace(",]", "]").replace(",}", "}")

            try:
                recibo_json = json.loads(json_string)
                '''Added an id to identify the order'''
                recibo_json['id'] = len(orders) + 1
                recibo_json['created_at'] = datetime.now().strftime("%a %b %d %Y %I:%M:%S %p")
                recibo_json['status'] = 'PENDING'
                info_logger.info(f'JSON generado: {json_string}')
            except json.JSONDecodeError as e:
                error_logger.exception(f'Error al decodificar JSON: {e}')
                recibo_json = None

            if recibo_json:
                orders.append(recibo_json)                
                info_logger.info(f'Recibo almacenado en recibos: {str(orders)}')

            response_text = response_text.replace(json_string, '').strip()
        else:
            info_logger.info(f'No se encontró un JSON válido en la respuesta')
            info_logger.info(response_text)
        # Enviar respuesta consolidada
        #reply_message(number, response_text)
    except Exception as e:
        error_logger.exception(f"Error al procesar mensajes: {e}")
        response_text = 'Lo siento, no puedo procesar tu solicitud en este momento.'
        #reply_message(number, "Lo siento, no pude procesar tu solicitud.")
    finally:
        # Limpiar buffer y timer
        reply_message(json.dumps({
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': number,
            'type': 'text',
            'text': {
                'body': response_text
            }
        }))
        messages_buffer[number] = []
        timers[number] = None


def manage_flow(message: str, number: str, message_id: str, name: str):
    '''Acumula mensajes y activa un temporizador'''
    global messages_buffer, timers
    
    if not ai_status['status']:
        return ''
    
    # Primero: marca el mensaje como leído si el message_id es diferente
    # de <WHATSAPP_MESSAGE_ID>
    if message_id != '<WHATSAPP_MESSAGE_ID>':
        reply_message(json.dumps({
            'messaging_product': 'whatsapp',
            'status': 'read',
            'message_id':  message_id
        }))
    # Agregar mensaje al buffer
    if number in messages_buffer:
        messages_buffer[number].append((message, message_id))
    else:
        messages_buffer[number] = [(message, message_id)]

    # Iniciar temporizador si no existe
    if number not in timers or timers[number] is None:
        timers[number] = threading.Timer(5, ai_process_message, [number])
        timers[number].start()
    else: # Reiniciar temporizador
        timers[number].cancel()
        timers[number] = threading.Timer(5, ai_process_message, [number])
        timers[number].start()


def reply_message(data):
    '''Function that send messages or control the messages to WhatsApp Clients'''

    try:
        response = requests.post(
            app.config['WHATSAPP_URL'],
            headers={'Content-Type': 'application/json',
                     'Authorization': f"Bearer {app.config['WHATSAPP_TOKEN']}"},
            data=data)

        info_logger.info(f'Meta response: {response.content.decode()}')
        if response.status_code == 200:
            info_logger.info('Mensaje enviado. Status code: 200')
        else:
            error_logger.exception(f'Error al enviar mensaje. Status code: {response.status_code}')
    except Exception as ex:
        error_logger.exception(f'Error while trying do reply_message: {str(ex)}')
        raise ex

def get_message(message):
    '''Verify message send by user'''

    if 'type' not in message:
        text = 'Mensaje no reconocido'
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
        text = 'Mensaje no procesado'

    return text
