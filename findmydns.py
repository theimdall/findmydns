import os
import re
import subprocess
import ctypes
import requests

dns_server1 = []
dns_server2 = []
dns_serverProvider = []
ms_values = []
ms_vB_id = [0]
dns_File="dns_servers.txt"


def menu():
    is_Connected = is_connected()
    if is_Connected:
        dns_serverCurrent,dns_serverCurrentIp = dns_checkerCurrent()
    else:
        dns_serverCurrent,dns_serverCurrentIp = "Not Connected",""
    
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = "\033[34m" + r"""
   __ _           _                     _           
  / _(_)         | |                   | |          
 | |_ _ _ __   __| |_ __ ___  _   _  __| |_ __  ___ 
 |  _| | '_ \ / _` | '_ ` _ \| | | |/ _` | '_ \/ __|
 | | | | | | | (_| | | | | | | |_| | (_| | | | \__ \
 |_| |_|_| |_|\__,_|_| |_| |_|\__, |\__,_|_| |_|___/
                               __/ |                
                              |___/                 """ + f"""                                                                                                                                                                                                                                                                
            \033[33m[✔] https://github.com/theimdall/findmydns [✔]\033[0m
            [✔]            Version 1.0.0               [✔]

\033[32m[✔]Current DNS: {dns_serverCurrentIp}({dns_serverCurrent})\033[0m\n"""
    
    print(logo)
    option_list = [
        "Find My Dns",
        "Set My Dns",
        "Reset My Dns",
        "Exit",
    ]
    option_id = len(option_list)
    for a in range (0,len(option_list)):
        print(f'[{a}] {option_list[a]}')
    while option_id >= len(option_list):
        option_id = int(input("Option ==> "))
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    is_Connected = is_connected()
    if option_id == 0 and is_Connected:
        if os.path.exists(dns_File):
            read_dnsFile()
            dns_analysis()
        else:
            dns_FileNew = open("dns_servers.txt", "w")
            dns_FileNew.write("8.8.8.8,8.8.4.4,Google\n1.1.1.1,1.0.0.1,Cloudflare\n9.9.9.9,149.112.112.112,Quad9\n208.67.222.222,208.67.220.220,OpenDNS Home\n94.140.14.14,94.140.15.15,AdGuard DNS\n185.228.168.9,185.228.169.9,Clean Browsing\n76.76.19.19,76.223.122.150,Alternate DNS\n77.88.8.8,77.88.8.1,Yandex\n8.26.56.26,8.20.247.20,Comodo Secure\n76.76.2.0,76.76.10.0,Control D")
            dns_FileNew.close()
            print("dns_servers.txt file is not exist. New One Created!")
            read_dnsFile()
            dns_analysis()
    elif option_id == 1:
        dns_server1User = input("DNS1(ex. 8.8.8.8):")
        dns_server2User = input("DNS2(ex. 8.8.4.4):")
        dns_setU(dns_server1User,dns_server2User)
    elif option_id == 2:
        dns_reset()
    elif option_id == len(option_list)-1:
        exit()
        
def dns_analysis():
    for id,dns_s in zip(range(0,len(dns_server1)),dns_server1):
        is_Connected = is_connected()
        if is_Connected:
            ms_values.append(dns_checker(dns_s))
        else:
            exit()
        #print(dns_serverProvider[id],f":{ms_values[id]}ms")
        print(f"\033[32m{dns_serverProvider[id]}:{ms_values[id]}ms\033[0m")
    ms_vB = ms_values [:]
    print(ms_vB)
    for a in range (0,len(ms_values)-1):
        print(f"a:{a}")
        if ms_vB [a] < ms_vB[a+1] and a < len(ms_values)-1:
            if ms_vB[a] != ms_vB[a-1]:
                ms_vB_id[0] = a
                print("best_id:",ms_vB_id)
                ms_vB[a+1] = ms_vB[a]
            elif ms_vB[ms_vB_id[0]] == ms_vB[a]:
                print("best_id:",ms_vB_id)
                ms_vB[a+1] = ms_vB[a]
            print(f"a={a},{ms_vB[a]} < {ms_vB[a+1]}")   
            print("best_idSame:",ms_vB_id)
        elif ms_vB[a] > ms_vB[a+1] and a < len(ms_values)-2:
            ms_vB_id[0] = a+1
        
        else:
            ms_vB_id[0] = a+1
            print(f"elseWorked, a:{a},best_id:{ms_vB_id}")
        print(f"a={a}",ms_vB)
            
            
    print("best_id:",ms_vB_id)
    print("ms_values:",ms_values)
    for a in range(0,len(ms_values)):
        if ms_values[ms_vB_id[0]] == ms_values[a]:
            print("a")
            ms_vB_id.append(a)
        print("ms_vB_id",ms_vB_id)
    if len(ms_vB_id) > 2:
        print("Best Dns Servers:", end="")
        for a,b in zip(ms_vB_id[1:],range(1,len(ms_vB_id))):
                print(f"{b}){dns_serverProvider[a]}:{ms_values[a]}ms", end=" ")
        #print(f"{a}){dns_serverProvider[a]}:{ms_values[a]}ms", end=" ")
    else:
        print("BestDnsServer:",dns_serverProvider[ms_vB_id[0]],":",ms_values[ms_vB_id[0]])
    print("")
    isUserChangeDns = None
    while isUserChangeDns != "yes" and isUserChangeDns != "no":
        isUserChangeDns = str(input("Do you want to change your DNS settings(yes/no) :"))
    if isUserChangeDns == "yes":
        if len(ms_vB_id) > 2:
            dns_change_id = int(input("Which?:"))
            print(f"dns_change_id:{dns_change_id}")
            for a in range(1,len(ms_vB_id)):
                print(f"loopWorked:{a} times")
                print(f"dns_change_id:{dns_change_id}")
                if dns_change_id == a:
                    dns_change_id = ms_vB_id[a]
                    print("choosed:",dns_change_id)
                    print(f"DnsChoosed:{dns_serverProvider[dns_change_id]},{ms_values[dns_change_id]}, Informations:{dns_server1[dns_change_id]},{dns_server2[dns_change_id]}")
                    dns_set(dns_change_id)
        else:
            print(f"DnsChoosed:{dns_serverProvider[ms_vB_id[0]]},{ms_values[ms_vB_id[0]]}, Informations:{dns_server1[ms_vB_id[0]]},{dns_server2[ms_vB_id[0]]}")
            dns_set(ms_vB_id[0])
    elif isUserChangeDns == "no":
        print("Okey.")
                
    else:
        print("Incorrect choose") 
        menu()
        
def read_dnsFile():
    with open(dns_File,"r") as dns_FileSystem:
        for line in dns_FileSystem:
            parts = line.strip().split(',')
            if len(parts) >= 3: 
                dns_server1.append(parts[0])
                dns_server2.append(parts[1])
                dns_serverProvider.append(parts[2])
            
    return dns_server1,dns_server2,dns_serverProvider

def dns_checker(dns_serv):
    command = ["ping", dns_serv]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    outputCommand, _ = process.communicate()
    #print(outputCommand)
    ms_v = re.findall(r"Average = (\d+)ms", outputCommand.decode("utf-8"))
    if ms_v == None or ms_v == []:
            ms_v = [99999]
    ms_vC = [int(ms) for ms in ms_v]
    for ms_vs in ms_vC:
        ms_vC = ms_vs
    return ms_vC


def dns_checkerCurrent():
    command = "nslookup google.com"
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    outputCommand, _ = process.communicate()
    outputCommandDecoded = outputCommand.decode("utf-8")
    #print(outputCommandDecoded)
    output_serverNameInfo = re.search("Server:  ",outputCommandDecoded)
    output_serverIpInfo = re.search("Address:  ",outputCommandDecoded)
    output_midText = re.search("Name:",outputCommandDecoded)
    output_serverNameInfoLocation = output_serverNameInfo.end()
    output_serverIpInfoLocation = output_serverIpInfo.end()
    serverNameInfo = outputCommandDecoded[output_serverNameInfoLocation:output_serverIpInfo.start()-1].replace("\r","").replace("\n","").strip()
    serverIpInfo = outputCommandDecoded[output_serverIpInfoLocation:output_midText.start()].replace("\n","").replace("\r","").strip()
    return serverNameInfo,serverIpInfo

def dns_set(dns_id):
    commands = f'/k netsh interface ipv4 delete dnsservers "Wi-Fi" all & netsh interface ipv4 delete dnsservers "Ethernet" all & netsh interface ipv4 add dnsserver "Wi-Fi" address={dns_server1[dns_id]} index=1 & netsh interface ipv4 add dnsserver "Wi-Fi" address={dns_server2[dns_id]} index=2 & netsh interface ipv4 add dnsserver "Ethernet" address={dns_server1[dns_id]} index=1 & netsh interface ipv4 add dnsserver "Ethernet" address={dns_server2[dns_id]} index=2 & exit'
    #commandsT = f'/k netsh interface ipv4 delete dnsservers "Wi-Fi" all & netsh interface ipv4 delete dnsservers "Ethernet" all & netsh interface ipv4 add dnsserver "Wi-Fi" address={dns_server1[dns_id]} index=1 & netsh interface ipv4 add dnsserver "Wi-Fi" address={dns_server2[dns_id]} index=2 & netsh interface ipv4 add dnsserver "Ethernet" address={dns_server1[dns_id]} index=1 & netsh interface ipv4 add dnsserver "Ethernet" address={dns_server2[dns_id]} index=2 & netsh interface ip show config'
    ctypes.windll.shell32.ShellExecuteW(
            None,
            u"runas",
            u"cmd.exe",
            commands,
            None,
            1
        )
    input("Process Completed.Press any button for Menu...")
    menu()

def dns_setU(dns_s1,dns_s2):
    commands = f'/k netsh interface ipv4 delete dnsservers "Wi-Fi" all & netsh interface ipv4 delete dnsservers "Ethernet" all & netsh interface ipv4 add dnsserver "Wi-Fi" address={dns_s1} index=1 & netsh interface ipv4 add dnsserver "Wi-Fi" address={dns_s2} index=2 & netsh interface ipv4 add dnsserver "Ethernet" address={dns_s1} index=1 & netsh interface ipv4 add dnsserver "Ethernet" address={dns_s2} index=2 & exit'
    #commandsT = f'/k netsh interface ipv4 delete dnsservers "Wi-Fi" all & netsh interface ipv4 delete dnsservers "Ethernet" all & netsh interface ipv4 add dnsserver "Wi-Fi" address={dns_server1[dns_id]} index=1 & netsh interface ipv4 add dnsserver "Wi-Fi" address={dns_server2[dns_id]} index=2 & netsh interface ipv4 add dnsserver "Ethernet" address={dns_server1[dns_id]} index=1 & netsh interface ipv4 add dnsserver "Ethernet" address={dns_server2[dns_id]} index=2 & netsh interface ip show config'
    ctypes.windll.shell32.ShellExecuteW(
            None,
            u"runas",
            u"cmd.exe",
            commands,
            None,
            1
        )
    input("Process Completed. Press any button for Menu...")
    menu()
    
def dns_reset():
    commands = f'/k netsh interface ipv4 delete dnsservers "Wi-Fi" all & netsh interface ipv4 delete dnsservers "Ethernet" all  & exit'
    #commandsT = f'/k netsh interface ipv4 delete dnsservers "Wi-Fi" all & netsh interface ipv4 delete dnsservers "Ethernet" all & netsh interface ip show config'
    ctypes.windll.shell32.ShellExecuteW(
            None,
            u"runas",
            u"cmd.exe",
            commands,
            None,
            1
        )
    input("Process Completed. Press any button for Menu...")
    menu()

def is_connected():
    try:
        requests.get('https://www.google.com')
        return True
    except requests.exceptions.RequestException:
        print("No Internet Connection")
        return False


    

menu()