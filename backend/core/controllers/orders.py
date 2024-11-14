from flask import abort
from core.app import orders
from apiflask import APIBlueprint
from core.schemas.orders import OrderStatusSchema, OrdersSchema
from core.schemas.utils import MessageSchema


bp = APIBlueprint('orders', __name__)


@bp.get('/orders/<string:status>')
@bp.output(OrdersSchema)
def get_orders(status: str):
  '''Method to get the orders'''
  global orders

  try:
      the_orders = orders
      if status != 'ALL':
         the_orders = [order for order in orders if order['status'] == status]
      return {'orders': the_orders}
  except Exception as ex:
      abort(str(ex))

@bp.put('/orders/<string:id>')
@bp.input(OrderStatusSchema)
@bp.output(MessageSchema)
def update_order(id, json_data):
   '''Method to update the state of the order.
   
   It could be:
   From PENDING to -> COMPLETE.
   '''
   global orders
   
   try:
      '''Here it should be a connection with the database and send the new state.
      Meanwhile we are going to make it with a cicle'''
      the_orders = orders
      the_orders[int(id) - 1]['status'] = json_data['status']
      orders = the_orders
      return {'message': 'Saved successfully'}
   except Exception as ex:
      abort(str(ex))