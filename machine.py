from telnetlib import Telnet
from dataclasses import dataclass

@dataclass
class MachineInfo:
    host : str
    name : str
    output : str = "Awaiting"
    cancel : bool = False
    useprint : bool = True

    result = None
    future = None
    config = None

    def globalname(self) -> str:
        return f"{self.host}:{self.name}"


#Little wrapper to remove annoying b-strings

class Machine(Telnet):

    end = "\n"

    def result(self,res):  
        self.info.result = int(res)


    def output(self,out):  
        if self.info.useprint:
            print(out)
            return 
        self.info.output = out

    def info_obj(self,info):
        self.info = info

    def write(self,output,end=None):
        if end == None:
            end = self.end

        super().write(output.encode("ascii") + end.encode("ascii"))

    def read_until(self,output,timeout=5,ret=False):
        if self.info.cancel:
            raise Exception("Cancelled")
        if type(output) != bytes:
            output = output.encode("ascii")
        res = super().read_until(output,timeout) or b""
        if not ret:
            return (output in res)
        else:
            return res.decode("utf-8")
