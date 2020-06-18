from math import pow

answers = 0

def unmark(num):
    global answers
    answers -= int(pow(2,num-1))


def mark(num):
    global answers
    answers |= int(pow(2,num-1))


def main(shell):
    global answers
    shell.wrait("terminal length 0")
    res1 = shell.wrait("")
    if ("FW#" in res1):
        mark(1)

    res1 = shell.wrait("show ip interface vlan 1")
    res2 = shell.wrait("show ip interface vlan 2")
    if ("address is 192.168.1.2/24" in res1) and ("address is 192.168.1.2/24" in res2):
        mark(2)

    shell.wrait("configure teminal")
    shell.wrait("ip domain lookup")
    shell.wrait("\x04")

    mark(3)
    ress = []
    ress.append(shell.wrait("wsr.left"))
    ress.append(shell.wrait("rtr-a.wsr.left"))
    ress.append(shell.wrait("rtr-b.wsr.left"))
    ress.append(shell.wrait("rtr-central.wsr.left"))
    for res in ress:
        if ("unable to find computer address" in res):
            unmark(3)
            break
            


    return answers