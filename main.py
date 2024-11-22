import socket
import requests
from socketserver import BaseRequestHandler, UDPServer, ThreadingMixIn

# DNS server settings
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 53  # DNS typically uses port 53

# Fake IP to respond with if a domain is blocked
BLOCKED_IP = '0.0.0.0'

# Load the blocklist from Steven Black's Unified Hosts file
def load_blocklist(url):
    try:
        response = requests.get(url)
        blocklist = set()
        for line in response.text.split('\n'):
            if line.startswith('0.0.0.0') or line.startswith('127.0.0.1'):
                parts = line.split()
                if len(parts) >= 2:
                    blocklist.add(parts[1].strip())
        return blocklist
    except requests.exceptions.RequestException as e:
        print(f"Error fetching blocklist: {e}")
        return set()  # Return an empty blocklist in case of error

blocklist = load_blocklist('https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts')

# Enhance UDPServer to allow address reuse
class ReusableUDPServer(ThreadingMixIn, UDPServer):
    allow_reuse_address = True

class DNSRequestHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        sock = self.request[1]  # Renaming variable to avoid shadowing the socket module
        client_address = self.client_address
        dns_header = data[:12]

        try:
            # Parsing the domain from the DNS query
            question_section = data[12:]
            first_zero = question_section.index(b'\x00')
            domain_parts = []
            i = 0
            while i < first_zero:
                length = question_section[i]
                i += 1
                domain_parts.append(question_section[i:i+length])
                i += length
            domain = b'.'.join(domain_parts).decode('utf-8')
            
            if domain.lower() in blocklist:
                # Domain is blocked, respond with BLOCKED_IP
                print(f"[BLOCKED] {domain} - {client_address[0]}")
                response = dns_header + b'\x81\x83' + data[12:] + b'\x00\x00\x00\x00\x00\x04' + bytes(map(int, BLOCKED_IP.split('.')))
                sock.sendto(response, client_address)
            else:
                # Forward the DNS query to a public DNS server and relay the response
                print(f"[FORWARD] {domain} - {client_address[0]}")
                forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                forward_socket.sendto(data, ('8.8.8.8', 53))
                response, _ = forward_socket.recvfrom(1024)
                sock.sendto(response, client_address)
                forward_socket.close()
        except Exception as e:
            print(f"Exception handling DNS request: {e}")
            
if _name_ == "_main_":
    while True:
        try:
            server = ReusableUDPServer((HOST, PORT), DNSRequestHandler)
            print("DNS server running on port", PORT)
            print("Blocking", len(blocklist), "domains")
            server.serve_forever()
        except OSError as e:
            if e.errno == 98:
                print(f"Port {PORT} is already in use. Trying an alternative port.")
                PORT += 1  # Try the next port
                server.server_close()
            else:
                raise e
