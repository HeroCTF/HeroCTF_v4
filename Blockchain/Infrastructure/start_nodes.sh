#!/bin/bash

# First node is the miner. As you unlock the account, it's super unsafe to use it as a public endpoint
geth --datadir node1/ --syncmode "full" --allow-insecure-unlock --port 30311  --networkid 1337 --unlock "[ACCOUNT_ADDRESS]" --password node1/password --txpool.pricelimit "2" --mine --miner.gasprice 0 > node0.log &
# Second node is public, not mining, with no unlocked account. 
geth --datadir node2/ --syncmode "full" --allow-insecure-unlock --port 30312 --http --http.addr "0.0.0.0" --http.port 8502 --http.api "personal,net,eth,web3,txpool,miner" --http.corsdomain "*" --networkid 1337 > node2.log &

echo OK
