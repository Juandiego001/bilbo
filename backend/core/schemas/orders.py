from apiflask import fields, Schema


class OrderSchema(Schema):
  id = fields.String()
  name = fields.String()
  products = fields.List(fields.String())
  quantity = fields.List(fields.Integer())
  address = fields.String()
  description = fields.String()
  phone = fields.String()
  payment_method = fields.String()
  created_at = fields.String()
  status = fields.String()


class OrderStatusSchema(Schema):
  status = fields.String()

class OrdersSchema(Schema):
  orders = fields.List(fields.Nested(OrderSchema))