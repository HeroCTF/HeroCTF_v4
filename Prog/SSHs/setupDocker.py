from os import rename, remove
from secrets import choice
import subprocess
from string import hexdigits


# Variables
NB_USERS = 250
PASS_LENGTH = 20
CODE = """#include <iostream>
#include <fstream>
#include <string>
using namespace std;int main(){string line;ifstream myfile("/home/$USER/.ssh/id_rsa");if (myfile.is_open()){while(getline(myfile,line)){cout << line << '\\n';}myfile.close();}return 0;}
"""

# Create first user
subprocess.Popen(f"useradd -m -d /home/user1 -s /bin/bash user1 && echo 'user1:password123' | chpasswd", shell=True).communicate()


# Main
for i in range(2, NB_USERS+1):
    # Create credentials
    user = f"user{i}"
    password = ''.join(choice(hexdigits) for i in range(PASS_LENGTH))

    # Create user
    subprocess.Popen(f"useradd -m -d /home/{user} -s /bin/bash {user} && echo '{user}:{password}' | chpasswd && chmod 700 /home/{user}", shell=True).communicate()

    # Create keys
    subprocess.Popen(f"su {user} -c 'ssh-keygen -b 4096 -t rsa -f ~/.ssh/id_rsa -q -N \"\" && mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys'", shell=True).communicate()

    # Compile binary
    open("/root/tmp.cpp", "w").write(CODE.replace("$USER", user))
    subprocess.Popen(f"g++ /root/tmp.cpp -o /home/user{i-1}/getSSHKey", shell=True).communicate()

    # Change owner and set SUID
    subprocess.Popen(f"chown {user} /home/user{i-1}/getSSHKey && chmod +s /home/user{i-1}/getSSHKey", shell=True).communicate()

    print(f"[*] User {i}/{NB_USERS}")
    
rename("/root/flag.txt", f"/home/user{NB_USERS}/flag.txt")
remove("/usr/bin/su")
