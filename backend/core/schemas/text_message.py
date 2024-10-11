from apiflask import Schema, fields


class ProfileSchema(Schema):
    name = fields.String()


class ContactSchema(Schema):
    profile = fields.Nested(ProfileSchema)
    wa_id = fields.String()


class TextSchema(Schema):
    body = fields.String()


class MessageSchema(Schema):
    from_ = fields.String(data_key='from', attribute='from')
    id = fields.String()
    timestamp = fields.String()
    text = fields.Nested(TextSchema)
    type = fields.String()


class MetadataSchema(Schema):
    display_phone_number = fields.String()
    phone_number_id = fields.String()


class ValueSchema(Schema):
    messaging_product = fields.String()
    metadata = fields.Nested(MetadataSchema)
    contacts = fields.List(fields.Nested(ContactSchema))
    messages = fields.List(fields.Nested(MessageSchema))


class ChangesSchema(Schema):
    value = fields.Nested(ValueSchema)
    field = fields.String()


class EntrySchema(Schema):
    id = fields.String()
    changes = fields.List(fields.Nested(ChangesSchema))


class TextMessageSchema(Schema):
    object = fields.String()
    entry = fields.List(fields.Nested(EntrySchema))