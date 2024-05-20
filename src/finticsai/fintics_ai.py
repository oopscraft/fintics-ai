from flask import Flask, jsonify, request, abort, render_template
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch

app = Flask(__name__)

@app.route('/chat', methods = ['GET'])
def get_ai():
    return render_template('chat.html')

@app.route('/assets/<string:asset_id>', methods = ['POST'])
def create_asset(asset_id):
    asset = {}
    return jsonify(asset), 201

@app.route('/assets/<string:asset_id>', methods = ['GET'])
def get_asset(asset_id):
    asset = {
        'asset_id': 'test',
        'asset_name': 'name'
    }
    return jsonify(asset)

if __name__ == '__main__':
    app.run(debug=True)
