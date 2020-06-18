ANSWERS="0"

function mark(){
ANSWERS=$(($ANSWERS | (2**($1-1))))
}

echo "##[Checking Hostname]##"
[ `hostname` == "SRV" ] && mark 1

# IP Configuration example

echo "##[Checking interfaces]##"
ping -W 1 -c 8 172.16.20.100 > /dev/null 2>&1 && \ # Interface configured
ping -W 1 -c 8 172.16.20.1 > /dev/null 2>&1 && \
mark 2

# DNS Example

echo "##[Checking DNS Forward]##"
[[ `systemctl is-active bind9` == 'active' ]] && \
dig wsr.left && \
dig rtr-a.wsr.left && \
dig rtr-b.wsr.left && \
dig rtr-central.wsr.left && \
mark 3

echo "##[Checking DNS Reverse]##"
[[ `systemctl is-active bind9` == 'active' ]] && \
dig -x 172.16.20.100 && \
dig -x 172.16.50.1 && \
dig -x 172.16.100.1 && \
dig -x 172.16.55.2 && \
dig -x 172.16.200.1 && \
dig -x 172.16.10.2 && \
dig -x 172.16.20.1 && \
dig -x 172.16.50.1 && \
dig -x 172.16.55.1 && \
mark 4

#Mount checking example

echo "##[Checking mounting]##"
[[ `mount | grep /dev/sda` ]] && mark 5

#Sysctl example

echo "##[Checking sysctl]##"
[ `cat /proc/sys/net/ipv4/ip_forward` == 0 ] && mark 6

#Web page check

echo "##[Checking webpage]##"
[[ `curl router.lan | grep 'LuCI - Lua Configuration Interface'` ]] && mark 7

echo "##[ready]##"

echo "###{"$ANSWERS"}###"
