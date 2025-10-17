#!/usr/bin/env python3
"""
IDOR & AUTHORIZATION TESTER - REAL IDOR VULNERABILITY DISCOVERY
Tests for Insecure Direct Object References and authorization bypasses
"""
import requests
import re
import json
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class IDORTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.vulnerabilities = []
        
    def test_all_idor(self):
        """Test all IDOR techniques"""
        print(f"[*] Starting IDOR testing on {self.target_url}")
        
        self.test_numeric_id_idor()
        self.test_uuid_idor()
        self.test_object_level_authorization()
        self.test_function_level_authorization()
        self.test_path_traversal_idor()
        
        return self.vulnerabilities
    
    def test_numeric_id_idor(self):
        """Test numeric ID IDOR"""
        print("[*] Testing numeric ID IDOR...")
        
        # Extract numeric IDs from URL
        ids = self._extract_numeric_ids(self.target_url)
        
        for id_param, id_value in ids:
            # Test sequential IDs
            test_ids = [
                int(id_value) - 1,
                int(id_value) + 1,
                1, 2, 3, 100, 1000
            ]
            
            for test_id in test_ids:
                try:
                    test_url = self._replace_id_in_url(self.target_url, id_param, str(test_id))
                    response = self.session.get(test_url, timeout=10)
                    
                    if self._check_idor_vulnerability(response, test_id):
                        self.vulnerabilities.append({
                            "type": "Numeric ID IDOR",
                            "severity": "High",
                            "url": test_url,
                            "parameter": id_param,
                            "test_value": test_id
                        })
                except:
                    pass
    
    def test_uuid_idor(self):
        """Test UUID IDOR"""
        print("[*] Testing UUID IDOR...")
        
        # Extract UUIDs from URL
        uuids = self._extract_uuids(self.target_url)
        
        test_uuids = [
            "00000000-0000-0000-0000-000000000001",
            "11111111-1111-1111-1111-111111111111",
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        ]
        
        for uuid_param, uuid_value in uuids:
            for test_uuid in test_uuids:
                try:
                    test_url = self._replace_id_in_url(self.target_url, uuid_param, test_uuid)
                    response = self.session.get(test_url, timeout=10)
                    
                    if self._check_idor_vulnerability(response, test_uuid):
                        self.vulnerabilities.append({
                            "type": "UUID IDOR",
                            "severity": "High",
                            "url": test_url,
                            "parameter": uuid_param,
                            "test_value": test_uuid
                        })
                except:
                    pass
    
    def test_object_level_authorization(self):
        """Test object-level authorization"""
        print("[*] Testing object-level authorization...")
        
        # Test different HTTP methods
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        
        for method in methods:
            try:
                response = self.session.request(method, self.target_url, timeout=10)
                
                if response.status_code == 200 and method in ["PUT", "PATCH", "DELETE"]:
                    self.vulnerabilities.append({
                        "type": "Object-Level Authorization Bypass",
                        "severity": "Critical",
                        "url": self.target_url,
                        "method": method
                    })
            except:
                pass
    
    def test_function_level_authorization(self):
        """Test function-level authorization"""
        print("[*] Testing function-level authorization...")
        
        # Test admin endpoints
        admin_paths = [
            "/admin", "/administrator", "/dashboard",
            "/api/admin", "/api/users", "/api/settings",
            "/manage", "/control-panel"
        ]
        
        parsed = urlparse(self.target_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        for path in admin_paths:
            try:
                test_url = base_url + path
                response = self.session.get(test_url, timeout=10)
                
                if response.status_code == 200 and "admin" in response.text.lower():
                    self.vulnerabilities.append({
                        "type": "Function-Level Authorization Bypass",
                        "severity": "Critical",
                        "url": test_url
                    })
            except:
                pass
    
    def test_path_traversal_idor(self):
        """Test path traversal IDOR"""
        print("[*] Testing path traversal IDOR...")
        
        payloads = [
            "../admin",
            "../../admin",
            "../../../admin",
            "../user/1",
            "../../user/1",
        ]
        
        for payload in payloads:
            try:
                test_url = self.target_url + "/" + payload
                response = self.session.get(test_url, timeout=10)
                
                if self._check_idor_vulnerability(response, payload):
                    self.vulnerabilities.append({
                        "type": "Path Traversal IDOR",
                        "severity": "High",
                        "url": test_url,
                        "payload": payload
                    })
            except:
                pass
    
    def _extract_numeric_ids(self, url):
        """Extract numeric IDs from URL"""
        ids = []
        
        # Extract from path
        path_parts = urlparse(url).path.split("/")
        for i, part in enumerate(path_parts):
            if part.isdigit():
                ids.append((f"path_{i}", part))
        
        # Extract from query parameters
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        for key, values in params.items():
            for value in values:
                if value.isdigit():
                    ids.append((key, value))
        
        return ids
    
    def _extract_uuids(self, url):
        """Extract UUIDs from URL"""
        uuids = []
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        
        matches = re.findall(uuid_pattern, url, re.IGNORECASE)
        for match in matches:
            uuids.append(("uuid", match))
        
        return uuids
    
    def _replace_id_in_url(self, url, param, new_value):
        """Replace ID in URL"""
        if param.startswith("path_"):
            # Replace in path
            parts = url.split("/")
            index = int(param.split("_")[1])
            if index < len(parts):
                parts[index] = new_value
            return "/".join(parts)
        else:
            # Replace in query parameters
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            params[param] = [new_value]
            new_query = urlencode(params, doseq=True)
            return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    
    def _check_idor_vulnerability(self, response, test_value):
        """Check if IDOR vulnerability exists"""
        indicators = [
            response.status_code == 200,
            len(response.text) > 100,
            "user" in response.text.lower() or "profile" in response.text.lower(),
            "error" not in response.text.lower(),
            "unauthorized" not in response.text.lower(),
            "forbidden" not in response.text.lower()
        ]
        return sum(indicators) >= 4

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 idor_tester.py <url>")
        sys.exit(1)
    
    tester = IDORTester(sys.argv[1])
    vulns = tester.test_all_idor()
    
    print(f"\n[+] Found {len(vulns)} potential IDOR vulnerabilities")
    for vuln in vulns:
        print(f"  - {vuln['type']}: {vuln['severity']}")

