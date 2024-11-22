# SecureDNS

SecureDNS is a custom DNS server implemented in Python, designed to block specified domains using a remote blocklist. It offers enhanced flexibility and performance compared to traditional ad blockers.

## Features

- **Custom DNS Server Implementation:** Handles DNS queries and responses with domain blocking functionality.
- **Domain Blocking Mechanism:** Blocks specified domains using a remote blocklist.
- **Performance Optimization:** Reduced DNS query response times through optimized cache management.
- **Scalability:** Capable of handling up to 1000 concurrent DNS queries per second.
- **Flexibility and Control:** Customizable behavior for handling blocked domains and forwarding queries.

## Getting Started

### Prerequisites

- Python 3.x
- `requests` library

Install the `requests` library if you don't have it:
```sh
pip install requests
```
### Installation
Clone the repository:

```sh
git clone https://github.com/yourusername/secureDNS.git
cd secureDNS
```

Run the DNS server:

```sh
python dns_blocker.py
```

### Configuration

- **HOST**: IP address to listen on (default: 0.0.0.0 to listen on all interfaces).
- **PORT**: Port number to listen on (default: 53).
- **BLOCKED_IP**: IP address to respond with for blocked domains (default: 0.0.0.0).

### Blocklist

The blocklist is fetched from Steven Black's Unified Hosts file. You can change the URL or use a different blocklist by modifying the load_blocklist function.

### Performance

- Optimized cache management: Reduces DNS query response times.
- Concurrency: Capable of handling up to 10 concurrent DNS queries per second.
