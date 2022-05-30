# Hero Chain !

## What's in all that ?  
    
The `deployer/` folder contains all the environment that allows to automatically deploy smart contracts.   
The `website/`folder contains the entire Melcoin website.

You will find all the solves (in JS) under `deployer/test_challenge_*.js`

## How to start that ?

```bash

# setup the nodes
./init_nodes.sh

# start the nodes
./start_nodes.sh

# /!\ Important
# You have to note down the node1/ enode address add manually add it to the second node via geth

geth attach node2/geth.ipc
```
Then, once in the geth console :
```js
admin.addPeer("enode://[NODE1_ADDRESS]")
```

Just start the website in another terminal if you want to
```
cd website
pip install -r requirements.txt
python App.py
```
