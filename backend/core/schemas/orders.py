from apiflask import fields, Schema


class ProductsSchema(Schema):
  id = fields.Integer()
  name = fields.String()
  price = fields.Number()
  quantity = fields.Integer()


class OrderSchema(Schema):
  id = fields.Integer()
  name = fields.String()
  address = fields.String()
  description = fields.String()
  phone = fields.String()
  payment_method = fields.String()
  products = fields.List(fields.Nested(ProductsSchema))
  created_at = fields.String()
  status = fields.String()


class OrderStatusSchema(Schema):
  status = fields.String()


class OrdersSchema(Schema):
  orders = fields.List(fields.Nested(OrderSchema))


class OrderQuerySchema(Schema):
  id = fields.Integer()
  name = fields.String()
  phone = fields.String()
  payment_method = fields.String(data_key='paymentMethod')
  products = fields.List(fields.Integer())
  initial_date = fields.String(data_key='initialDate')
  final_date = fields.String(data_key='finalDate')
  status = fields.String()