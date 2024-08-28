import socket
import struct
import platform

def ip_to_int(ip_address):
    return struct.unpack("!I", socket.inet_aton(ip_address))[0]

def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack("!I", ip_int))

def is_valid_ip(ip_address):
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False

def get_default_gateway():
    if platform.system().lower() == 'windows':
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces') as key:
            return winreg.QueryValueEx(key, "DefaultGateway")[0][0]
    else:
        import netifaces
        gateways = netifaces.gateways()
        return gateways['default'][netifaces.AF_INET][0]