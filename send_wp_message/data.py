data = {
    'object': 'whatsapp_business_account',
    'entry': [ # data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        {
            'id': '<WHATSAPP_BUSINESS_ACCOUNT_ID>',  # Reemplaza con el ID de tu cuenta de WhatsApp Business
            'changes': [
                {
                    'value': {
                        'messaging_product': 'whatsapp',
                        'metadata': {
                            'display_phone_number': '<BUSINESS_DISPLAY_PHONE_NUMBER>',  # Reemplaza con el número público
                            'phone_number_id': '<BUSINESS_PHONE_NUMBER_ID>'  # Reemplaza con el ID del número de teléfono
                        },
                        'contacts': [
                            {
                                'profile': {
                                    'name': '<WHATSAPP_USER_NAME>'  # Reemplaza con el nombre del usuario de WhatsApp
                                },
                                'wa_id': '<WHATSAPP_USER_ID>'  # Reemplaza con el ID de usuario de WhatsApp
                            }
                        ],
                        'messages': [
                            { 
                                'from': '<WHATSAPP_NUMBER>',  # Número desde el cual se envía el mensaje # data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                                'id': '<WHATSAPP_MESSAGE_ID>',  # Reemplaza con el ID del mensaje
                                'timestamp': '<WEBHOOK_SENT_TIMESTAMP>',  # Reemplaza con la marca de tiempo
                                'text': {
                                    'body': '<MESSAGE>'
                                },
                                'type': 'text'
                            }
                        ]
                    },
                    'field': 'messages'
                }
            ]
        }
    ]
}