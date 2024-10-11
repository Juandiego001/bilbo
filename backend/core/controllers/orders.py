from flask import abort
from core.app import orders
from apiflask import APIBlueprint
from core.schemas.orders import OrdersSchema


bp = APIBlueprint('orders', __name__)


@bp.get('/orders')
@bp.output(OrdersSchema)
def get_orders():
  '''Method to get the orders'''

  try:
    return {'orders': orders}
  except Exception as ex:
      abort(str(ex))

