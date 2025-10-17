#!/usr/bin/env python3
"""
Port Scanner - Fast and efficient port scanning utility
Author: Safouan Benali
License: MIT
"""

import socket
import threading
import argparse
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple

class PortScanner:
    """Fast and efficient port scanner with concurrent scanning capabilities."""
    
    def __init__(self, target: str, timeout: float = 1.0, max_threads: int = 100):
        self.target = target
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = []
        self.scan_results = []
    
    def scan_port(self, port: int) -> Dict:
        """Scan a single port and return results."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            
            if result == 0:
                service = self.get_service_name(port)
                return {
                    'port': port,
                    'status': 'open',
                    'service': service,
                    'timestamp': time.time()
                }
            else:
                return {
                    'port': port,
                    'status': 'closed',
                    'service': None,
                    'timestamp': time.time()
                }
        except Exception as e:
            return {
                'port': port,
                'status': 'error',
                'service': None,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def get_service_name(self, port: int) -> str:
        """Get common service name for port."""
        common_ports = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 993: 'IMAPS',
            995: 'POP3S', 3389: 'RDP', 5432: 'PostgreSQL', 3306: 'MySQL',
            6379: 'Redis', 27017: 'MongoDB', 9200: 'Elasticsearch'
        }
        return common_ports.get(port, 'Unknown')
    
    def scan_ports(self, start_port: int, end_port: int) -> List[Dict]:
        """Scan a range of ports concurrently."""
        print(f"Scanning {self.target} from port {start_port} to {end_port}")
        print(f"Using {self.max_threads} threads with {self.timeout}s timeout")
        
        ports = list(range(start_port, end_port + 1))
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_port = {executor.submit(self.scan_port, port): port for port in ports}
            
            for future in as_completed(future_to_port):
                result = future.result()
                self.scan_results.append(result)
                
                if result['status'] == 'open':
                    open_ports.append(result)
                    print(f"✓ Port {result['port']} ({result['service']}) is open")
        
        return sorted(open_ports, key=lambda x: x['port'])
    
    def scan_common_ports(self) -> List[Dict]:
        """Scan common ports."""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 6379, 27017, 9200]
        return self.scan_ports(min(common_ports), max(common_ports))
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive scan report."""
        open_ports = [r for r in self.scan_results if r['status'] == 'open']
        closed_ports = [r for r in self.scan_results if r['status'] == 'closed']
        error_ports = [r for r in self.scan_results if r['status'] == 'error']
        
        return {
            'target': self.target,
            'scan_time': time.time(),
            'total_ports_scanned': len(self.scan_results),
            'open_ports': len(open_ports),
            'closed_ports': len(closed_ports),
            'error_ports': len(error_ports),
            'open_ports_list': open_ports,
            'scan_duration': max([r['timestamp'] for r in self.scan_results]) - min([r['timestamp'] for r in self.scan_results]) if self.scan_results else 0
        }

def main():
    parser = argparse.ArgumentParser(description='Fast and efficient port scanner')
    parser.add_argument('-t', '--target', required=True, help='Target host to scan')
    parser.add_argument('-p', '--ports', help='Port range to scan (e.g., 1-1000 or 80,443,8080)')
    parser.add_argument('--common', action='store_true', help='Scan only common ports')
    parser.add_argument('--timeout', type=float, default=1.0, help='Connection timeout in seconds')
    parser.add_argument('--threads', type=int, default=100, help='Number of concurrent threads')
    parser.add_argument('-o', '--output', help='Output file for results (JSON format)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize scanner
    scanner = PortScanner(args.target, args.timeout, args.threads)
    
    # Determine ports to scan
    if args.common:
        open_ports = scanner.scan_common_ports()
    elif args.ports:
        if '-' in args.ports:
            start, end = map(int, args.ports.split('-'))
            open_ports = scanner.scan_ports(start, end)
        else:
            ports = [int(p) for p in args.ports.split(',')]
            open_ports = []
            for port in ports:
                result = scanner.scan_port(port)
                scanner.scan_results.append(result)
                if result['status'] == 'open':
                    open_ports.append(result)
    else:
        print("Please specify ports with -p or use --common for common ports")
        return
    
    # Generate report
    report = scanner.generate_report()
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print("\n" + "="*50)
        print(f"SCAN RESULTS FOR {args.target.upper()}")
        print("="*50)
        print(f"Open ports: {len(open_ports)}")
        print(f"Total scanned: {report['total_ports_scanned']}")
        print(f"Scan duration: {report['scan_duration']:.2f} seconds")
        print("\nOpen Ports:")
        for port in open_ports:
            print(f"  {port['port']}/tcp - {port['service']}")

if __name__ == "__main__":
    main()
