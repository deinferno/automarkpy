from re import findall,search
from machine import Machine
from time import sleep
from uuid import uuid4
from base64 import b64encode

class LinuxShell(Machine):

    maximumserialsize = 1024-128

    #simple inefficient hacky modem with built in tools only
    def send_executable(self,path):
        randomname = "".join(set(uuid4().hex))
        self.write("\n\x03\n")
        script = open(path,"r").read()
        script.replace("[[RANDOMNAME]]",randomname)
        scriptb64 = b64encode(bytes(script,"utf-8"))
        self.output(f"Transmitting file {path}")
        
        spllist = findall(r".{1,%d}" % self.maximumserialsize, scriptb64.decode("utf-8"))

        index = 0
        llen = len(spllist)
        while index < llen:
                str = spllist[index]
                self.write(f" base64 -d << EOF >> /tmp/{randomname} && echo R{index}")
                self.read_until(">")
                self.write(str+"\nEOF")
                self.output(f"Sending file part {index+1}/{len(spllist)}")
                if not self.read_until("R%d" % index , 1):
                        continue
                index += 1

        self.output("Uploaded")
        
        return randomname

    def execute(self,remotename):
        self.output("Executing")
        self.write(f" bash /tmp/{remotename}")
        str = ""
        res = None
        while True:
            str += self.read_until("\x00",1,True)
            res = search(r"###\{(.*)\}###",str)
            if res:
                break
            res = findall(r"##\[(.*)\]##",str)
            if res and res[res.__len__()-1]:
                self.output("Shell: "+res[res.__len__()-1])

        self.output("Result is "+res.group(1))

        self.result(res.group(1))
        

    def login(self,user,password = None,defpassword = None):
        for i in range(1,8):
            self.output(f"Login attempt {i}")

            self.write("\x03\x03\x03\x04\x04\x04",end="")
            
            self.read_until("login:")
            self.output("Entering user")
            self.write(user)
            if i > 4:
                self.output("Attempting with default password")
                password = defpassword
            if password:
                self.read_until("Password:")
                self.output("Entering password")
                self.write(password)

            output = self.read_until("Login incorrect",3,True)
            if output and ("Password:" not in output)  and ("Login incorrect" not in output):
                self.output("Login successful")
                return True

        raise Exception("Giving up trying to login")

            