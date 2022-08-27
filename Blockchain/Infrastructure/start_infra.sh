#!/bin/bash

if ! command -v "jq" &> /dev/null
then
    echo "jq could not be found, install before proceed again"
    exit
fi

./utils/clean.sh

# nodes
EXPOSE_IP="127.0.0.1"
NETWORK_ID=`jq '.config.chainId' utils/melchain.template`
JSON_RPC_PORT=8502
NODE1_PORT=30311
NODE2_PORT=30312

# webapp
WEBAPP_IP="127.0.0.1"
WEBAPP_PORT=22000

GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
BOLD=$(tput bold)
NC=$(tput sgr0)

mkdir node1

# Create password for account on blockchain
read -sp "Password for account: " password
echo
echo

echo $password > node1/password

# Generate account and get public key
res=`geth account new --keystore node1/keystore --password node1/password 2>/dev/null`
pub_key=`echo $res | grep -o -P 'key:\s+0x.{40}' | cut -d "x" -f2 | awk '{print tolower($0)}'`

echo "0x$pub_key" > pub_key.txt

# Replacement in extraData allows created account to be part of sealers
# Replacement in alloc object allows to credit our previously created account with the amount specified in balance
sed "s/{ALLOC_ADDR}/$pub_key/g" utils/melchain.template > melchain.json

# init nodes
geth --datadir node1/ init melchain.json &> node1_init.log
echo "(${GREEN}✔️${NC}) Node 1 initialized with genesis block"

geth --datadir node2/ init melchain.json &> node2_init.log
echo "(${GREEN}✔️${NC}) Node 2 initialized with genesis block"
echo

# start nodes
geth --datadir node1/ --nat=extip:$EXPOSE_IP --syncmode "full" --allow-insecure-unlock --port $NODE1_PORT  --networkid $NETWORK_ID --unlock "0x$pub_key" --password node1/password --txpool.pricelimit "2" --mine --miner.gasprice 0 &> node1.log &
echo "(${GREEN}✔️${NC}) Node 1 started"

geth --datadir node2/ --nat=extip:$EXPOSE_IP --syncmode "full" --allow-insecure-unlock --port $NODE2_PORT --http --http.addr "$EXPOSE_IP" --http.port $JSON_RPC_PORT --http.api "personal,net,eth,web3,txpool,miner" --http.corsdomain "*" --networkid $NETWORK_ID &> node2.log &
echo "(${GREEN}✔️${NC}) Node 2 started"

# wait for nodes to start completly
sleep 5

miner_node=`geth --exec 'admin.nodeInfo.enode' attach node1/geth.ipc`
echo $miner_node > miner_node.txt

geth --exec "admin.addPeer($miner_node)" attach node2/geth.ipc &>/dev/null

# get private key used to deploy contracts
keystore_file=`ls node1/keystore | tail -1`
keystore_path=`readlink -f node1/keystore/$keystore_file`
private_key=`./utils/get_private_key.py $keystore_path`

echo "PRIVATE_KEY=\"$private_key\"" > deployer/.env

cat << EOF > website/.env
JSON_RPC_URL="http://$EXPOSE_IP:$JSON_RPC_PORT"
ACCOUNT_ADDRESS="0x$pub_key"
HTTP_IP="$WEBAPP_IP"
HTTP_PORT="$WEBAPP_PORT"
EOF

cat << EOF

Blockchain as been deployed with JSON-RPC URL as: ${BOLD}http://$EXPOSE_IP:$JSON_RPC_PORT${NC} on chain ID ${BOLD}$NETWORK_ID${NC}

Account used to interact with blockchain has following informations:

${BOLD}Public key${NC}          ${GREEN}0x$pub_key${NC}
${BOLD}Private key${NC}         ${GREEN}0x$private_key${NC}
${BOLD}Password file at${NC}    ${GREEN}node1/password${NC}
EOF

