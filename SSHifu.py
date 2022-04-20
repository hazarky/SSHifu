import os
import subprocess

string = input("Please enter a string with quotes: ")
string = string.replace('\"', "\"")
os.system(" ssh zathras@ger-kali0 \"sudo -- sh -c \'mv /var/log/auth.log /var/log/.oldlog\'\"")
os.system(" ssh zathras@ger-kali0 \"sudo -- sh -c \'ln -s /dev/null /var/log/auth.log \'\"")


os.system(" ssh zathras@ger-kali0 \"sudo -- sh -c \'" + string + "\'\"")
pwd = subprocess.check_output("ssh zathras@ger-kali0 pwd", shell=True)
pwd = str(pwd.decode("utf-8").split("'")).rstrip("\\n']")
pwd = str(pwd.strip("[\'"))
hostname = subprocess.check_output("ssh zathras@ger-kali0 hostname", shell=True)
hostname = str(hostname.decode("utf-8").split("'")).rstrip("\\n']")
hostname = str(hostname.strip("[\'"))
username = subprocess.check_output("ssh zathras@ger-kali0 whoami", shell=True)
username = str(username.decode("utf-8").split("'")).rstrip("\\n']")
username = str(username.strip("[\'"))

while True:
    string = input(username + "@"+hostname+":"+pwd + "> ")
    if string == "EXIT":
        print("exiting session\nGoodbye..")
        os.system(" ssh zathras@ger-kali0 \"sudo -- sh -c \'rm -rf /var/log/auth.log \'\"")
        os.system(" ssh zathras@ger-kali0 \"sudo -- sh -c \'mv /var/log/.oldlog /var/log/auth.log \'\"")
        exit()
    string = string.replace('\"', "\"")
    os.system(" ssh zathras@ger-kali0 \"sudo -- sh -c \'" + string + "\'\"")
    pwd = subprocess.check_output("ssh zathras@ger-kali0 pwd", shell=True)
    pwd = str(pwd.decode("utf-8").split("'")).rstrip("\\n']")
    pwd = str(pwd.strip("[\'"))  
