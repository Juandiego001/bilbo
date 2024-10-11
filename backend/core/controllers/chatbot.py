from core.app import app
from flask import request, abort
from apiflask import APIBlueprint
from core.schemas.chatbot import VerificationRequest
from core.schemas.text_message import TextMessageSchema
from core.services import chatbot


bp = APIBlueprint('chatbot', __name__)


@bp.get('/webhook')
@bp.input(VerificationRequest, location='query')
def check_token(query_data):
    '''Verify input token'''

    try:
        mode = query_data['mode']
        verify_token = query_data['verify_token']
        challenge = query_data['challenge']

        if (mode == "subscribe" and verify_token == app['WEBHOOK_VERIFY_TOKEN']):
            return challenge
        else:
            raise Exception()
    except:
        abort(403)


@bp.post('/webhook')
@bp.input(TextMessageSchema)
def get_messages(json_data):
    '''Get messages'''

    try:
        value = json_data['entry'][0]['changes'][0]['value']
        message = value['messages'][0]
        to = message['from']
        message_id = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        message_text = message['text']['body']
        
        chatbot.manage_flow(message_text, to, message_id, name)
        return 'Sent'
    except Exception as e:
        abort('Not sent ' + str(e))
