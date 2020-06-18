from re import findall,search
from machine import Machine
from time import sleep
from uuid import uuid4
from base64 import b64encode
from os.path import dirname,basename,splitext
from sys import path

class CiscoShell(Machine):

    end = "\r\n"

    #not needed as cisco's tcl is really limited and we better off with python
    def send_executable(self,relpath):
        path.append(dirname(relpath))
        relpath = splitext(basename(relpath))[0]
        return relpath

    def execute(self,relpath):
        script = getattr(__import__(relpath, fromlist=["main"]), "main")
        self.output("Executing")
        res = script(self)
        self.output(f"Result is {res}")
        self.result(res)
        
    def wrait(self,out,end=None):
        self.write(out,end)
        return self.read_until("#",ret=True)

    def login(self,user,password = None,defpassword = None):
        enablepassword = None
        if "\\" in password:
            data = password.split("\\")
            password = data[0]
            enablepassword = data[1]
            self.output("Enable password specified")
        for i in range(1,8):
            self.output(f"Login attempt {i}")

            self.write("")
            self.write("")
            if not self.read_until("#"):
                while True:
                    self.write("")
                    self.write("")
                    self.write("")
                    if self.read_until("User Access Verification",1):
                        break
                    self.write("\x04\x04\x04",end="")
                    if self.read_until("User Access Verification",1):
                        break
                    self.write("exit")
                    self.write("exit")
            
            self.read_until("Username:",1)
            self.output("Entering user")
            self.write(user)
            if i > 4:
                self.output("Attempting with default password")
                password = defpassword
            if password:
                self.read_until("Password:")
                self.output("Entering password")
                self.write(password)


            output = self.read_until("Login invalid",3,True)
            if output and ("now available" not in output) and \
                          ("Username:" not in output) and \
                          ("Password:" not in output)  and \
                          ("Login invalid" not in output):
                self.output("Login successful")

                if enablepassword:
                    self.output("Elevating priviledges")
                    self.write("enable")
                    self.read_until("Password:")
                    self.write(enablepassword)
                    self.read_until("#")
                    self.output("Elevated")

                return True

        raise Exception("Giving up trying to login")

            