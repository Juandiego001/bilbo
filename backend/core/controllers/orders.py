from flask import abort
from core.app import orders
from apiflask import APIBlueprint
from core.schemas.orders import OrderStatusSchema, OrdersSchema, \
   OrderQuerySchema
from core.schemas.utils import MessageSchema


bp = APIBlueprint('orders', __name__)


@bp.get('/orders')
@bp.input(OrderQuerySchema, location='query')
@bp.output(OrdersSchema)
def get_orders(query_data: str):
    '''Method to get the orders'''
    global orders

    try:
        status = query_data['status']
        the_orders = orders

        # Filter by status
        if status != 'ALL':
            the_orders = [
                order for order in orders if order['status'] == status]

        print('\nQUERY DATA:\n')
        print(query_data)
        print('\n\n')

        '''
        Búsquedas temporales en listas.
        A futuro, las búsquedas se harán directamente con base de datos.
        '''                            
        if 'id' in query_data and query_data['id'] != '':
            the_orders = [each_order for each_order in the_orders if each_order['id'] == query_data['id']]
        if 'name' in query_data and query_data['name'] != '':
            the_orders = [each_order for each_order in the_orders if query_data['name'].upper() in (each_order['name'].upper())]
        if 'phone' in query_data and query_data['phone'] != '':
            the_orders = [each_order for each_order in the_orders if query_data['phone'] in each_order['phone']]
        if 'payment_method' in query_data and query_data['payment_method'] != '':
            the_orders = [each_order for each_order in the_orders if each_order['payment_method'] == query_data['payment_method']]
        # if 'products' in query_data and query_data['id'] != '':
        #     the_orders = [each_order for each_order in the_orders if each_order['id'] == query_data['id']]
        # if 'created_at' in query_data and query_data['created_at'] != '':
        #     the_orders = [each_order for each_order in the_orders if each_order['id'] == query_data['id']]
         
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
