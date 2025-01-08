from flask import Flask, render_template, jsonify, request
import time
import hashlib

# Define Block class
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

# Define Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Initialize Flask app and blockchain
app = Flask(__name__)
blockchain = Blockchain()

# Route for rendering the HTML dashboard
@app.route('/')
def index():
    return render_template('index.html')

# API to view the entire blockchain
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash
        })
    return jsonify({'chain': chain_data, 'length': len(blockchain.chain)})

# API to add a new block
@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'Data is required'}), 400
    blockchain.add_block(data)
    return jsonify({'message': 'Block added successfully'})

# API to validate the blockchain
@app.route('/validate', methods=['GET'])
def validate_blockchain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({'is_valid': is_valid})

if __name__ == '__main__':
    app.run(debug=True)
