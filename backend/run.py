from core.app import app, HOST, PORT
from core.controllers.chatbot import bp as bp_chatbot
from core.controllers.orders import bp as bp_orders
from core.controllers.products import bp as bp_products


app.register_blueprint(bp_chatbot, url_prefix='/')
app.register_blueprint(bp_orders, url_prefix='/orders')
app.register_blueprint(bp_products, url_prefix='/products')


if __name__ == '__main__':
  app.run(host=HOST, port=PORT, debug=True)