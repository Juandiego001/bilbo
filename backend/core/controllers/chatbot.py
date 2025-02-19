from core.app import app, ai_status, info_logger, error_logger
from flask import abort
from apiflask import APIBlueprint
from core.schemas.chatbot import AiStatusSchema, VerificationRequest
from core.schemas.text_message import TextMessageSchema
from core.schemas.utils import MessageSchema
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

        if (mode == "subscribe" and verify_token == app.config['WEBHOOK_VERIFY_TOKEN']):
            return challenge
        
        raise Exception()
    except Exception as ex:
        error_logger.exception(f'There was an error with the /api/chatbot/webhook endpoint: {str(ex)}')
        abort(403)


@bp.post('/webhook')
@bp.input(TextMessageSchema)
@bp.output(MessageSchema)
def get_messages(json_data):
    '''Get messages'''

    try:
        value = json_data['entry'][0]['changes'][0]['value']
        message_obj = value['messages'][0]
        number = message_obj['from']
        message_id = message_obj['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        message = message_obj['text']['body']

        response = chatbot.manage_flow(message, number, message_id, name)

        info_logger.info(f'Number: {number} Message: {message}')
        info_logger.info(f'To: {number} AI Response: {response}')

        return {'message': response}
    except Exception as e:
        abort('Not sent ' + str(e))


@bp.get('/ai-status')
@bp.output(AiStatusSchema)
def get_ai_status():
    '''Get AI Status'''

    global ai_status

    try:
        return {'status': ai_status['status']}
    except Exception as ex:
        abort(str(ex))


@bp.put('/ai-status')
@bp.input(AiStatusSchema)
@bp.output(MessageSchema)
def set_ai_status(json_data):
    '''Set AI Status'''
    
    global ai_status

    try:
        ai_status['status'] = json_data['status']
        return {'message': 'Saved successfully'}
    except Exception as ex:
        abort(str(ex))