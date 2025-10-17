# Port Scanner

## Overview
The Port Scanner is a fast and efficient Python script for network port scanning with concurrent processing capabilities. It provides comprehensive port scanning with service detection, banner grabbing, and JSON output format.

## Features
- ✅ Fast concurrent scanning with configurable threads
- ✅ Service detection and banner grabbing
- ✅ Custom port ranges and common ports
- ✅ JSON output format
- ✅ Real-time progress reporting
- ✅ Error handling and timeout management

## Usage

### Basic Usage
```bash
# Scan specific port range
python scripts/network/port_scanner.py -t 192.168.1.1 -p 1-1000

# Scan common ports
python scripts/network/port_scanner.py -t example.com --common

# Scan specific ports
python scripts/network/port_scanner.py -t example.com -p 80,443,8080
```

### Advanced Usage
```bash
# High-speed scanning with custom timeout
python scripts/network/port_scanner.py -t 192.168.1.0/24 -p 1-1000 --threads 200 --timeout 0.5

# Save results to file
python scripts/network/port_scanner.py -t example.com -p 1-1000 -o scan_results.json

# Verbose output
python scripts/network/port_scanner.py -t example.com --common -v
```

## Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--target` | `-t` | Target host to scan | Required |
| `--ports` | `-p` | Port range or comma-separated ports | Required* |
| `--common` | | Scan only common ports | False |
| `--timeout` | | Connection timeout in seconds | 1.0 |
| `--threads` | | Number of concurrent threads | 100 |
| `--output` | `-o` | Output file for results | None |
| `--verbose` | `-v` | Verbose output | False |

*Required unless using `--common`

## Examples

### 1. Basic Network Scan
```bash
# Scan a single host
python scripts/network/port_scanner.py -t 192.168.1.1 -p 1-1000

# Output:
# Scanning 192.168.1.1 from port 1 to 1000
# Using 100 threads with 1.0s timeout
# ✓ Port 22 (SSH) is open
# ✓ Port 80 (HTTP) is open
# ✓ Port 443 (HTTPS) is open
```

### 2. Web Server Scan
```bash
# Scan common web ports
python scripts/network/port_scanner.py -t example.com -p 80,443,8080,8443

# Scan with service detection
python scripts/network/port_scanner.py -t example.com --common
```

### 3. Network Range Scan
```bash
# Scan multiple hosts
for ip in 192.168.1.{1..10}; do
    echo "Scanning $ip:"
    python scripts/network/port_scanner.py -t $ip --common
done
```

### 4. Integration with Other Tools
```bash
# Save results and process with jq
python scripts/network/port_scanner.py -t example.com --common -o results.json
jq '.open_ports_list[] | select(.service == "HTTP")' results.json
```

## Output Format

### Console Output
```
Scanning example.com from port 1 to 1000
Using 100 threads with 1.0s timeout
✓ Port 80 (HTTP) is open
✓ Port 443 (HTTPS) is open

==================================================
SCAN RESULTS FOR EXAMPLE.COM
==================================================
Open ports: 2
Total scanned: 1000
Scan duration: 2.34 seconds

Open Ports:
  80/tcp - HTTP
  443/tcp - HTTPS
```

### JSON Output
```json
{
  "target": "example.com",
  "scan_time": 1640995200.0,
  "total_ports_scanned": 1000,
  "open_ports": 2,
  "closed_ports": 998,
  "error_ports": 0,
  "open_ports_list": [
    {
      "port": 80,
      "status": "open",
      "service": "HTTP",
      "timestamp": 1640995200.0
    },
    {
      "port": 443,
      "status": "open",
      "service": "HTTPS",
      "timestamp": 1640995200.0
    }
  ],
  "scan_duration": 2.34
}
```

## Common Ports Scanned

When using `--common`, the scanner checks these ports:
- **21** - FTP
- **22** - SSH
- **23** - Telnet
- **25** - SMTP
- **53** - DNS
- **80** - HTTP
- **110** - POP3
- **143** - IMAP
- **443** - HTTPS
- **993** - IMAPS
- **995** - POP3S
- **3389** - RDP
- **5432** - PostgreSQL
- **3306** - MySQL
- **6379** - Redis
- **27017** - MongoDB
- **9200** - Elasticsearch

## Performance Tips

### 1. Optimize Thread Count
```bash
# For local networks (fast)
python scripts/network/port_scanner.py -t 192.168.1.1 -p 1-1000 --threads 200

# For internet targets (slower)
python scripts/network/port_scanner.py -t example.com -p 1-1000 --threads 50
```

### 2. Adjust Timeout
```bash
# Fast scan (may miss some ports)
python scripts/network/port_scanner.py -t example.com -p 1-1000 --timeout 0.5

# Thorough scan (slower but more accurate)
python scripts/network/port_scanner.py -t example.com -p 1-1000 --timeout 3.0
```

### 3. Batch Processing
```bash
# Scan multiple targets efficiently
targets=("192.168.1.1" "192.168.1.2" "192.168.1.3")
for target in "${targets[@]}"; do
    python scripts/network/port_scanner.py -t $target --common -o "scan_${target}.json" &
done
wait
```

## Security Considerations

### Legal and Ethical Use
- ✅ **Use only on systems you own or have permission to test**
- ✅ **Respect rate limits** to avoid overwhelming targets
- ✅ **Follow responsible disclosure** practices
- ❌ **Never scan systems without authorization**
- ❌ **Never use for malicious purposes**

### Best Practices
1. **Start with common ports** to avoid overwhelming targets
2. **Use appropriate timeouts** to balance speed and accuracy
3. **Respect network policies** and rate limits
4. **Document your scans** for audit purposes
5. **Use VPN when appropriate** for anonymity

## Troubleshooting

### Common Issues

#### 1. Connection Refused
```bash
# Check if target is reachable
ping example.com
telnet example.com 80
```

#### 2. Timeout Issues
```bash
# Increase timeout for slow networks
python scripts/network/port_scanner.py -t example.com -p 1-1000 --timeout 5.0
```

#### 3. Permission Denied
```bash
# Some systems require root privileges for raw sockets
sudo python scripts/network/port_scanner.py -t example.com -p 1-1000
```

#### 4. Firewall Blocking
```bash
# Try different ports or use VPN
python scripts/network/port_scanner.py -t example.com -p 80,443,8080
```

### Debug Mode
```bash
# Enable verbose output for troubleshooting
python scripts/network/port_scanner.py -t example.com -p 1-1000 -v
```

## Dependencies
- Python 3.8+
- No additional Python packages required
- Network connectivity to target

## Related Scripts
- [SSL Certificate Checker](ssl_check.md) - SSL/TLS certificate analysis
- [Backup Scanner](backup_scanner.md) - Database backup discovery
- [Advanced Vulnerability Scanner](../web/advanced_vulnerability_scanner.md) - Web vulnerability testing

## License
MIT License - See [LICENSE](../../LICENSE) for details
