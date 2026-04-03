#!/usr/bin/env python3
"""ipmath - IPv4/IPv6 subnet calculator and IP math. Zero dependencies."""
import sys, struct, socket

def ip_to_int(ip):
    try:
        return int.from_bytes(socket.inet_pton(socket.AF_INET, ip), 'big'), 4
    except OSError:
        return int.from_bytes(socket.inet_pton(socket.AF_INET6, ip), 'big'), 6

def int_to_ip(n, ver=4):
    if ver == 4:
        return socket.inet_ntop(socket.AF_INET, n.to_bytes(4, 'big'))
    return socket.inet_ntop(socket.AF_INET6, n.to_bytes(16, 'big'))

def parse_cidr(cidr):
    if '/' not in cidr:
        ip, ver = ip_to_int(cidr)
        prefix = 32 if ver == 4 else 128
        return ip, prefix, ver
    ip_str, prefix = cidr.rsplit('/', 1)
    prefix = int(prefix)
    ip, ver = ip_to_int(ip_str)
    return ip, prefix, ver

def subnet_info(cidr):
    ip, prefix, ver = parse_cidr(cidr)
    bits = 32 if ver == 4 else 128
    mask = ((1 << bits) - 1) ^ ((1 << (bits - prefix)) - 1)
    network = ip & mask
    broadcast = network | ((1 << (bits - prefix)) - 1)
    total = 1 << (bits - prefix)
    usable = max(total - 2, 0) if ver == 4 and prefix < 31 else total

    print(f"Address:    {int_to_ip(ip, ver)}")
    print(f"Network:    {int_to_ip(network, ver)}/{prefix}")
    print(f"Netmask:    {int_to_ip(mask, ver)}")
    if ver == 4:
        print(f"Broadcast:  {int_to_ip(broadcast, ver)}")
        if prefix < 31:
            print(f"First host: {int_to_ip(network + 1, ver)}")
            print(f"Last host:  {int_to_ip(broadcast - 1, ver)}")
    print(f"Total IPs:  {total:,}")
    if ver == 4 and prefix < 31:
        print(f"Usable:     {usable:,}")
    print(f"Version:    IPv{ver}")

def contains(cidr, ip_str):
    net, prefix, ver = parse_cidr(cidr)
    ip, ver2 = ip_to_int(ip_str)
    if ver != ver2:
        print("Version mismatch"); return
    bits = 32 if ver == 4 else 128
    mask = ((1 << bits) - 1) ^ ((1 << (bits - prefix)) - 1)
    result = (ip & mask) == (net & mask)
    print(f"{'Yes' if result else 'No'} — {ip_str} is {'in' if result else 'NOT in'} {cidr}")

def range_cmd(cidr):
    net, prefix, ver = parse_cidr(cidr)
    bits = 32 if ver == 4 else 128
    mask = ((1 << bits) - 1) ^ ((1 << (bits - prefix)) - 1)
    network = net & mask
    count = 1 << (bits - prefix)
    limit = min(count, 256)
    for i in range(limit):
        print(int_to_ip(network + i, ver))
    if count > 256:
        print(f"... ({count - 256:,} more)")

def add_cmd(ip_str, offset):
    ip, ver = ip_to_int(ip_str)
    print(int_to_ip(ip + int(offset), ver))

def usage():
    print("""ipmath - IPv4/IPv6 subnet calculator

Usage:
  ipmath info <CIDR>           Subnet details
  ipmath contains <CIDR> <IP>  Check if IP is in subnet
  ipmath range <CIDR>          List IPs (max 256)
  ipmath add <IP> <offset>     Add offset to IP

Examples:
  ipmath info 192.168.1.0/24
  ipmath contains 10.0.0.0/8 10.5.3.1
  ipmath add 192.168.1.1 100
  ipmath info 2001:db8::/32""")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        usage(); sys.exit(0)
    cmd = args[0]
    try:
        if cmd == "info" and len(args) == 2:
            subnet_info(args[1])
        elif cmd == "contains" and len(args) == 3:
            contains(args[1], args[2])
        elif cmd == "range" and len(args) == 2:
            range_cmd(args[1])
        elif cmd == "add" and len(args) == 3:
            add_cmd(args[1], args[2])
        else:
            usage(); sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)
