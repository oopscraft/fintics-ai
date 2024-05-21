from flask import Flask
from finticsai.routes import chat
from finticsai.routes import news

# config

app = Flask(__name__)

# register module
app.register_blueprint(chat)
app.register_blueprint(news)


# @app.route('/chat', methods = ['GET'])
# def get_ai():
#     return render_template('chat.html')

# @app.route('/assets/<string:asset_id>', methods = ['POST'])
# def create_asset(asset_id):
#     asset = {}
#     return jsonify(asset), 201

# @app.route('/assets/<string:asset_id>', methods = ['GET'])
# def get_asset(asset_id):
#     asset = {
#         'asset_id': 'test',
#         'asset_name': 'name'
#     }
#     return jsonify(asset)

if __name__ == '__main__':
    app.run(debug=True)
