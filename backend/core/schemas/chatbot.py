from apiflask import Schema, fields


class VerificationRequest(Schema):
    mode = fields.String(data_key='hub.mode')
    verify_token = fields.String(data_key='hub.verify_token')
    challenge = fields.String(data_key='hub.challenge')

class AiStatusSchema(Schema):
    status = fields.Boolean()