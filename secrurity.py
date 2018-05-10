import os 

#Create iptables v4 file with the appropriate rules
def ipv4():
    filed=("/etc/iptables.rules.v4");
    wfile=open(filed,"w");
    commands=("*filter",
            ":INPUT DROP [0:0]",
            ":FORWARD DROP [0:0]",
            ":OUTPUT ACCEPT [93:10245]",
            "-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT", #ssh
            "-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT",
            "-A INPUT -j DROP",
            "COMMIT");
    for i in commands:
        wfile.write(i+"\n");
    wfile.close();

# Create iptables v6 file with the appropriate rules
def ipv6():
    filed=("/etc/iptables.rules.v6");
    wfile=open(filed,"w");
    commands=("*filter",
            ":INPUT DROP [7:1338]",
            ":FORWARD DROP [0:0]",
            ":OUTPUT ACCEPT [104:17563]",
            "-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT", #ssh
            "-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT",
            "-A INPUT -p ipv6-icmp -j ACCEPT",
            "COMMIT");
    for i in commands:
        wfile.write(i+"\n");
    wfile.close();

#Create a file which will startup rules after every reboot
#version 4
def startup4():
    saveto=("/etc/network/if-pre-up.d/iptablesv4");
    wfile=open(saveto,"w");
    script4=("#!/bin/sh","/sbin/iptables-restore < /etc/iptables.rules.v4");
    for i in script4:
        wfile.write(i+"\n");
    wfile.close();
    os.system("chmod +x"+" "+saveto); 

#version 6
def startup6():
    saveto=("/etc/network/if-pre-up.d/iptablesv6");  
    wfile=open(saveto,"w");
    script6=("#!/bin/sh","/sbin/ip6tables-restore < /etc/iptables.rules.v6");
    for i in script6:
        wfile.write(i+"\n");
    wfile.close();
    os.system("chmod +x"+" "+saveto);

#Interact with the user
print("Enter 1 for iptables -v4 ");
print("Enter 2 for iptables -v6 ");
answ=input();

if(answ==1):
    ipv4();
    startup4();
elif(answ==2):
    ipv6();
    startup6();
else:
    print("Not known action! "); 

print ("Done !")
