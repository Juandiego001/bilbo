from apiflask import APIBlueprint
from flask import abort

bp = APIBlueprint(__name__)

@bp.get('/')
@bp.input()
def get_orders():
  '''Method to get the orders by status'''

  try:
    pass
  except Exception as ex:
      abort(str(ex))

