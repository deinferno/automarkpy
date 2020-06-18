$answers = 0

Function mark($int){
$script:answers = $script:answers -bor ([Math]::Pow(2,$int-1))
}

echo "##[Checking hostname]##"
If ($env:computername -eq "ServerCore"){mark 1}

echo "##[Checking interfaces]##"
If ((Test-Connection '172.16.20.100' -Count 1 -ErrorAction SilentlyContinue) -And `
(Test-Connection '172.16.20.1' -Count 1 -ErrorAction SilentlyContinue) ){mark 2}

#DNS Example

echo "##[Checking DNS Forward]##"
if ((Resolve-DnsName "wsr.left" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "rtr-a.wsr.left" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "rtr-b.wsr.left" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "rtr-central.wsr.left" -ErrorAction SilentlyContinue)){mark 3}

echo "##[Checking DNS Reverse]##"
if ((Resolve-DnsName "172.16.20.100" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "172.16.50.1" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "172.16.100.1" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "172.16.55.2" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "172.16.200.1" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "172.16.10.2" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "172.16.20.1" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "172.16.50.1" -ErrorAction SilentlyContinue) -And `
(Resolve-DnsName "172.16.55.1" -ErrorAction SilentlyContinue)
){mark 4}

#Spam it cause SAC can corrupt symbols
while ($true){
echo "###{$answers}###"
}