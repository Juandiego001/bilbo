from apiflask import Schema, fields

class MessageSchema(Schema):
  message = fields.String()