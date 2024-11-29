from flask import abort
from apiflask import APIBlueprint
from core.services.products import insert_product, update_product,\
  delete_product, get_all_products, get_product_info_by_id
from core.schemas.utils import MessageSchema
from core.schemas.products import ProductSchemaInUpdate, ProductSchemaInCreate,\
  ProductSchemaOut, ProductsSchemaOut

bp = APIBlueprint('products', __name__)

@bp.get('/')
@bp.output(ProductsSchemaOut)
def get_products():
  '''Get products'''

  try:
    return {'products': get_all_products()}
  except Exception as ex:
    abort(str(ex))


@bp.get('/detail/<string:id>')
@bp.output(ProductSchemaOut)
def get_product_detail(id):
  '''Get specific product'''

  try:
    return get_product_info_by_id(id)
  except Exception as ex:
    abort(str(ex))

@bp.patch('/<string:id>')
@bp.input(ProductSchemaInUpdate)
@bp.output(MessageSchema)
def update_products(id, json_data):
  '''Update products'''

  try:
    return update_product(id, json_data)
  except Exception as ex:
    abort(str(ex))

@bp.post('/')
@bp.input(ProductSchemaInCreate)
@bp.output(MessageSchema)
def create_products(json_data):
  '''Create products'''

  try:
    return insert_product(json_data)
  except Exception as ex:
    abort(str(ex))


@bp.delete('/<string:id>')
@bp.output(MessageSchema)
def delete_products(id):
  '''
  Delete products

  Set product status in False.
  '''

  try:
    return delete_product(id)
  except Exception as ex:
    abort(str(ex))