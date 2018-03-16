from flask import Flask, request
from blockchain import *

node = Flask(__name__)

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

blockchain = []
blockchain.append(create_genesis_block())


transaction_list = []
peer_nodes = []


@node.route('/transaction', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_transaction = request.get_json()

        transaction_list.append(new_transaction)
        
        print("New transaction")
        print("FROM: {}".format(new_txion['from']))
        print("TO: {}".format(new_txion['to']))
        print("AMOUNT: {}\n".format(new_txion['amount']))

        return "Transaction Successful!\n"

def is_not_prime(n):
    for i in range(2, int(n**0.5)+1):
        if (n % i) == 0:
            return True
    return False

def pow(last_proof):
    proof = last_proof + 1

    while (is_not_prime(proof)):
        proof += 1

    return proof


@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[-1]
    last_proof = last_block.data['proof-of-work']
    
    proof = pow(last_proof)

    transaction_list.append({
        "from" : "network",
        "to" : miner_address,
        "amount" : 1
        })
    new_block_data = {
        "proof-of-work" : proof,
        "transactions" : list(transaction_list)
        }

    new_block_index = last_block.index + 1
    new_block_timestamp = datetime.now()
    last_block_hash = last_block.hash 

    transaction_list[:] = []

    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
        )

    blockchain.append(mined_block)

    return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
       }) + "\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain
    
    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data =  str(block.data)
        block_hash = block.hash 
        block = {
          "index": block_index,
          "timestamp": block_timestamp,
          "data": block_data,
          "hash": block_hash
           }
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = request.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain

    blockchain = longest_chain



if __name__ == "__main__":
    node.run()