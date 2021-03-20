from src.blockchain import BlockChain

block_height = 1
MY_ADDRESSS = 'squeaky-cheese'

blockchain = BlockChain()
print(blockchain)

blockchain.create_transaction("alice", "bob", 1000)
blockchain.create_transaction("bob", "charlie", 500)

blockchain.mine(MY_ADDRESSS)
print(blockchain)


blockchain.create_transaction("alice", "bob", 60)
blockchain.create_transaction("bob", "charlie", 30)

blockchain.mine(MY_ADDRESSS)
print(blockchain)
