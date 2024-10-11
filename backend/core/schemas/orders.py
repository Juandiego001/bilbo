from apiflask import fields, Schema


class OrderSchema(Schema):
  name = fields.String()
  products = fields.List(fields.String())
  quantity = fields.List(fields.Integer())
  address = fields.String()
  description = fields.String()
  phone = fields.String()
  payment_method = fields.String()


class OrdersSchema(Schema):
  orders = fields.List(fields.Nested(OrderSchema))