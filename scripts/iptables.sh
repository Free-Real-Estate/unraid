# needs to be rewritten, used as temporary rules save
# you might want to use iptables-persistent in order to not mess with this

# disallow local
iptables -I DOCKER-USER -s 192.168.1.0/24 -j DROP
# allow router but not admin
iptables -I DOCKER-USER -s 192.168.1.1 -j ACCEPT
iptables -I DOCKER-USER -p tcp -s 192.168.1.1 --sport 80 --j DROP
# allow unraid proxy
iptables -I DOCKER-USER -s 192.168.1.30 -j ACCEPT
iptables -I DOCKER-USER -p tcp -s 192.168.1.30 ! --dport 80 --j DROP
# disallow containers to ssh host
iptables -A INPUT -p tcp --dport 22 --source 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP
# allow portainer to connect to unraid portainer agent
iptables -I DOCKER-USER -p tcp -s 192.168.1.30 --sport 9001 --j ACCEPT