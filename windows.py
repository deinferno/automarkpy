
from re import findall,search,split
from machine import Machine
from time import sleep
from uuid import uuid4
from base64 import b64encode

#Out of band windows control is awful
#Newline in EMS itself is \n and in windows is \r\n
#Character duplication bug make me loose 1 day of my life
#Serial wont respond to control characters except for Ctrl + C

class WindowsShell(Machine):

    end = "\r\n"

    def write(self,output,end=None):
        #https://docs.microsoft.com/en-us/azure/virtual-machines/troubleshooting/serial-console-windows
        prevchar = ""
        for char in output: # Fixes Windows Serial Console character duplication and loss
            if char == prevchar:
                sleep(0.8)
            prevchar = char
            super().write(char,end="")

        super().write("",end=end)

    maximumserialsize = 1024 - 64

    def send_executable(self,path):
        randomname = "".join(set(uuid4().hex))
        scriptb64 = b64encode(bytes(open(path,"r").read(),"utf-8"))
        self.output(f"Transmitting file {path}")
        
        spllist = findall(r".{1,%d}" % self.maximumserialsize, scriptb64.decode("utf-8"))

        sleep(5)

        while True:
            self.write("$output='';echo R-1")
            if self.read_until("R-1",4):
                break
        
        index = 0
        llen = len(spllist)
        while index < llen:
                    str = spllist[index]
                    self.write(f"$output+='{str}';echo R{index}")
                    self.output(f"Sending file part {index+1}/{len(spllist)}")
                    if not self.read_until(f"R{index}",4 ):
                        continue
                    index = index + 1

        self.output("Converting base64 to normal")

        self.write(f"[IO.File]::WriteAllBytes($env:temp+'\\{randomname}.ps1',[Convert]::FromBase64String($output));echo Done")

        self.read_until("Done")

        self.output("Uploaded")
        
        return randomname

    def execute(self,remotename):
        self.output("Executing")
        self.write(f"powershell -ExecutionPolicy bypass -File $env:temp\\{remotename}.ps1")
        str = ""
        res = None

        while True:
            str += self.read_until(b'\x00',1,True)
            res = search(r"###{(.*?)}###",str)
            if res:
                break
            res = findall(r"##\[(.*?)\]##",str)
            if res and res[res.__len__()-1]:
                self.output("Shell: "+res[res.__len__()-1])

        self.write("\x03")

        res = res.group(1)

        self.output(f"Result is {res}")

        self.result(res)

    def login(self,user,password,defpassword):
        domain = None
        if "\\" in user:
            data = user.split("\\")
            domain = data[0]
            user = data[1]
            self.output("Domain user")

        for i in range(1,8):
    
            self.output(f"Login attempt {i}")

            #Accessing CMD Login with SAC

            self.output("Getting SAC>")

            while True:

                for i in range(8):
                    self.write("\x03")

                if self.read_until("SAC>",3):
                    break

                for i in range(8):
                    self.write("exit")

                if self.read_until("SAC>",3):
                    break
                    
                for i in range(8):
                    self.write("") 

                if self.read_until("SAC>",3):
                    break

            self.end = "\n"

            for i in range(4):
                self.write("")

            self.read_until("SAC>")

            #CMD Channel

            self.output("CMD Channel")
            
            self.write("cmd")

            self.write("")

            self.read_until("A new channel",5)

            self.read_until("SAC>")

            self.write("ch -si 1")

            self.read_until("Use any other key")

            #CMD Login

            self.write("",end=" ")
        
            self.read_until("Username")
            self.output("Entering user")
            self.write(user)
            self.read_until("Domain")
            if domain:
                self.output("Entering domain")
                self.write(domain)
            else:
                self.output("Skipping domain")
                self.write("")
            if i > 4:
                self.output("Attempting with default password")
                password = defpassword
            if password:
                self.read_until("Password")
                self.output("Entering password")
                self.write(password)

            if not self.read_until("Microsoft Windows"):
                continue
            self.output("Login successful,entering powershell")
            
            self.end = "\r\n"
            
            self.write("powershell")

            self.write("Remove-Module PSReadLine")
            self.write("")

            self.read_until("PS",timeout=30)

            self.output("Powershell entered")

            return True

        raise Exception("Giving up trying to login")