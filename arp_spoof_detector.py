from scapy.all import Ether, ARP, srp, sniff, conf

"""
This function will make an ARP request
and retrieves the real MAC address the that IP address
"""

def get_mac(ip):
    """
    Returns the MAC address of `ip`, if it is unable to find it
    for some reason, throws `IndexError`
    """
    p = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    result = srp(p, timeout=3, verbose=False)[0]
    return result[0][1].hwsrc


"""
this function checks for ARP packets. More precisely,
ARP replies, and then compares between the real MAC address and the
response MAC address (that's sent in the packet itself).
"""

def process(packet):
    # if the packet is an ARP packet
    if packet.haslayer(ARP):
        # if it is an ARP response (ARP reply)
        if packet[ARP].op == 2:
            try:
                # get the real MAC address of the sender
                real_mac = get_mac(packet[ARP].psrc)
                # get the MAC address from the packet sent to us
                response_mac = packet[ARP].hwsrc
                
                # if they're different, definitely there is an attack
                if real_mac != response_mac:
                    print(f"[!] You are under attack, REAL-MAC: {real_mac.upper()}, FAKE-MAC: {response_mac.upper()}")
            
            except IndexError:
                # unable to find the real mac
                # may be a fake IP or firewall is blocking packets
                pass

sniff(store=False, prn=process)
            