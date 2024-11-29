import json
import re
import requests 
from datetime import datetime
from core.app import app, chat, info_logger, error_logger, orders, ai_status
from core.services.rag import rag 
from core.services.prompt import prompt

def ai_process_message(message: str):
    '''Process AI response'''

    try:
        content = rag(message)
        context = prompt(content, message)
        response_text = chat.send_message(message).text
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
            info_logger.info(f'No se encontró un JSON válido en la respuesta: {response_text}')
    except Exception as e:
        error_logger.exception(f'Error al procesar el mensaje: {e}')
        response_text = 'Lo siento, no puedo procesar tu solicitud en este momento.'
    finally:
        return response_text


def reply_message(data):
    '''Function that send messages or controll the messages to WhatsApp Clients'''

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


def manage_flow(message: str, number: str, message_id: str, name: str):
    '''Manage flow from a received'''

    # Si la IA no está activa se envía un mensaje vacío
    if not ai_status['status']:
        return ''
    
    # Primero: marca el mensaje como leído
    reply_message(json.dumps({
        'messaging_product': 'whatsapp',
        'status': 'read',
        'message_id':  message_id
    }))

    # Segundo: genera la respuesta de la IA
    ai_response = ai_process_message(message)

    # Tercero: envia la respuesta de la IA
    reply_message(json.dumps({
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': number,
        'type': 'text',
        'text': {
            'body': ai_response
        }
    }))

    return ai_response


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
