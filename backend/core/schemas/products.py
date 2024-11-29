from apiflask import fields, Schema


class ProductSchemaInCreate(Schema):
  nombre = fields.String()
  descripcion = fields.String()
  precio = fields.Number()
  disponibilidad = fields.Boolean()


class ProductSchemaInUpdate(Schema):
  nombre = fields.String(required=False)
  descripcion = fields.String(required=False)
  precio = fields.Number(required=False)
  disponibilidad = fields.Boolean(required=False)


class ProductSchemaOut(Schema):
  id = fields.Number()
  nombre = fields.String()
  descripcion = fields.String()
  precio = fields.Number()
  disponibilidad = fields.Boolean()


class ProductsSchemaOut(Schema):
  products = fields.List(fields.Nested(ProductSchemaOut))
