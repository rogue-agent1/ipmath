# ipmath

IPv4/IPv6 subnet calculator and IP math. Zero dependencies.

## Usage

```bash
# Subnet info
python3 ipmath.py info 192.168.1.0/24
python3 ipmath.py info 2001:db8::/32

# Check if IP is in subnet
python3 ipmath.py contains 10.0.0.0/8 10.5.3.1

# List IPs in range (max 256)
python3 ipmath.py range 192.168.1.0/30

# IP arithmetic
python3 ipmath.py add 192.168.1.1 100
```

## Features

- IPv4 and IPv6 support
- CIDR notation parsing
- Network/broadcast/mask calculation
- Containment checks
- IP range enumeration
- IP offset arithmetic
- Single file, zero dependencies
