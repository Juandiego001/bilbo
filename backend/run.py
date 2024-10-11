from core.app import app
from core.controllers.chatbot import bp as bp_chatbot
from core.controllers.orders import bp as bp_orders


app.register_blueprint(bp_chatbot, url_prefix='/')
app.register_blueprint(bp_orders, url_prefix='/orders')


if __name__ == '__main__':
  app.run(debug=True)