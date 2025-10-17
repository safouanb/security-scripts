#!/usr/bin/env python3
"""
BUSINESS LOGIC VULNERABILITY SCANNER - REAL BUG BOUNTY TOOL
Advanced business logic flaw detection for serious bug bounty hunting
"""
import os
import sys
import time
import json
import requests
import threading
import concurrent.futures
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
import re
import random
import string
from datetime import datetime

class BusinessLogicScanner:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.vulnerabilities = []
        self.endpoints = set()
        
    def test_idor_vulnerabilities(self, url):
        """Test for Insecure Direct Object References (IDOR)"""
        print(f"[*] Testing IDOR vulnerabilities: {url}")
        
        # Common IDOR patterns
        idor_patterns = [
            # User ID manipulation
            "user_id=1", "user_id=2", "user_id=3", "user_id=0", "user_id=-1",
            "id=1", "id=2", "id=3", "id=0", "id=-1",
            "uid=1", "uid=2", "uid=3", "uid=0", "uid=-1",
            
            # Document ID manipulation
            "doc_id=1", "doc_id=2", "doc_id=3", "doc_id=0", "doc_id=-1",
            "document_id=1", "document_id=2", "document_id=3", "document_id=0", "document_id=-1",
            "file_id=1", "file_id=2", "file_id=3", "file_id=0", "file_id=-1",
            
            # Order ID manipulation
            "order_id=1", "order_id=2", "order_id=3", "order_id=0", "order_id=-1",
            "order=1", "order=2", "order=3", "order=0", "order=-1",
            
            # Account ID manipulation
            "account_id=1", "account_id=2", "account_id=3", "account_id=0", "account_id=-1",
            "account=1", "account=2", "account=3", "account=0", "account=-1",
            
            # UUID manipulation
            "uuid=00000000-0000-0000-0000-000000000000",
            "uuid=11111111-1111-1111-1111-111111111111",
            "uuid=ffffffff-ffff-ffff-ffff-ffffffffffff",
        ]
        
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        for param_name, param_values in query_params.items():
            original_value = param_values[0]
            
            for pattern in idor_patterns:
                try:
                    test_url = url.replace(f"{param_name}={original_value}", f"{param_name}={pattern}")
                    response = self.session.get(test_url, timeout=10)
                    
                    # Check for different content (potential IDOR)
                    if response.status_code == 200 and response.text != "":
                        # Look for indicators of different user data
                        idor_indicators = [
                            "user", "email", "phone", "address", "profile",
                            "account", "balance", "credit", "payment",
                            "order", "invoice", "receipt", "transaction",
                            "document", "file", "attachment", "download",
                            "admin", "administrator", "root", "superuser"
                        ]
                        
                        if any(indicator in response.text.lower() for indicator in idor_indicators):
                            self.vulnerabilities.append({
                                'type': 'Insecure Direct Object Reference (IDOR)',
                                'severity': 'High',
                                'url': test_url,
                                'payload': pattern,
                                'parameter': param_name,
                                'description': f'Potential IDOR found in parameter {param_name}'
                            })
                            print(f"[!] Potential IDOR found: {test_url}")
                            
                except Exception as e:
                    continue
                    
        return False
    
    def test_race_conditions(self, url):
        """Test for race condition vulnerabilities"""
        print(f"[*] Testing race conditions: {url}")
        
        # Race condition test - multiple simultaneous requests
        def make_request():
            try:
                response = self.session.post(url, timeout=10)
                return response
            except:
                return None
        
        # Send multiple simultaneous requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [future.result() for future in concurrent.futures.as_completed(futures, timeout=15)]
        
        # Check for duplicate responses or unexpected behavior
        response_codes = [r.status_code for r in responses if r]
        if len(set(response_codes)) > 1:
            self.vulnerabilities.append({
                'type': 'Race Condition',
                'severity': 'Medium',
                'url': url,
                'payload': 'Multiple simultaneous requests',
                'parameter': 'N/A',
                'description': 'Potential race condition detected with multiple simultaneous requests'
            })
            print(f"[!] Potential race condition found: {url}")
            return True
            
        return False
    
    def test_business_logic_bypass(self, url):
        """Test for business logic bypasses"""
        print(f"[*] Testing business logic bypasses: {url}")
        
        # Common business logic bypass patterns
        bypass_patterns = [
            # Price manipulation
            "price=0", "price=-1", "price=0.01", "price=0.1",
            "amount=0", "amount=-1", "amount=0.01", "amount=0.1",
            "cost=0", "cost=-1", "cost=0.01", "cost=0.1",
            "total=0", "total=-1", "total=0.01", "total=0.1",
            
            # Quantity manipulation
            "quantity=0", "quantity=-1", "quantity=999999", "quantity=999999999",
            "qty=0", "qty=-1", "qty=999999", "qty=999999999",
            "count=0", "count=-1", "count=999999", "count=999999999",
            
            # Status manipulation
            "status=paid", "status=completed", "status=approved", "status=active",
            "state=paid", "state=completed", "state=approved", "state=active",
            "payment_status=paid", "payment_status=completed", "payment_status=approved",
            
            # Role manipulation
            "role=admin", "role=administrator", "role=superuser", "role=root",
            "user_type=admin", "user_type=administrator", "user_type=superuser",
            "permission=admin", "permission=administrator", "permission=superuser",
            
            # Date manipulation
            "date=2099-12-31", "date=2030-01-01", "date=2025-01-01",
            "expiry=2099-12-31", "expiry=2030-01-01", "expiry=2025-01-01",
            "expires=2099-12-31", "expires=2030-01-01", "expires=2025-01-01",
        ]
        
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        for param_name, param_values in query_params.items():
            original_value = param_values[0]
            
            for pattern in bypass_patterns:
                try:
                    test_url = url.replace(f"{param_name}={original_value}", f"{param_name}={pattern}")
                    response = self.session.get(test_url, timeout=10)
                    
                    # Check for successful bypass indicators
                    bypass_indicators = [
                        "success", "approved", "completed", "paid", "active",
                        "admin", "administrator", "superuser", "root",
                        "free", "discount", "promotion", "offer",
                        "unlimited", "premium", "pro", "enterprise"
                    ]
                    
                    if any(indicator in response.text.lower() for indicator in bypass_indicators):
                        self.vulnerabilities.append({
                            'type': 'Business Logic Bypass',
                            'severity': 'High',
                            'url': test_url,
                            'payload': pattern,
                            'parameter': param_name,
                            'description': f'Business logic bypass found in parameter {param_name}'
                        })
                        print(f"[!] Business logic bypass found: {test_url}")
                        
                except Exception as e:
                    continue
                    
        return False
    
    def test_authentication_bypass(self, url):
        """Test for authentication bypasses"""
        print(f"[*] Testing authentication bypasses: {url}")
        
        # Authentication bypass patterns
        auth_bypass_patterns = [
            # Token manipulation
            "token=", "token=null", "token=undefined", "token=0", "token=-1",
            "auth_token=", "auth_token=null", "auth_token=undefined", "auth_token=0",
            "access_token=", "access_token=null", "access_token=undefined", "access_token=0",
            "jwt=", "jwt=null", "jwt=undefined", "jwt=0",
            
            # Session manipulation
            "session_id=", "session_id=null", "session_id=undefined", "session_id=0",
            "session=", "session=null", "session=undefined", "session=0",
            "sid=", "sid=null", "sid=undefined", "sid=0",
            
            # User ID manipulation
            "user_id=0", "user_id=-1", "user_id=1", "user_id=2",
            "uid=0", "uid=-1", "uid=1", "uid=2",
            "id=0", "id=-1", "id=1", "id=2",
            
            # Role manipulation
            "role=admin", "role=administrator", "role=superuser", "role=root",
            "user_role=admin", "user_role=administrator", "user_role=superuser",
            "permission=admin", "permission=administrator", "permission=superuser",
            
            # Admin bypass
            "admin=true", "admin=1", "admin=yes", "admin=on",
            "is_admin=true", "is_admin=1", "is_admin=yes", "is_admin=on",
            "administrator=true", "administrator=1", "administrator=yes", "administrator=on",
        ]
        
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        for param_name, param_values in query_params.items():
            original_value = param_values[0]
            
            for pattern in auth_bypass_patterns:
                try:
                    test_url = url.replace(f"{param_name}={original_value}", f"{param_name}={pattern}")
                    response = self.session.get(test_url, timeout=10)
                    
                    # Check for authentication bypass indicators
                    auth_bypass_indicators = [
                        "dashboard", "admin", "administrator", "superuser", "root",
                        "profile", "account", "settings", "configuration",
                        "users", "members", "customers", "clients",
                        "orders", "transactions", "payments", "billing",
                        "reports", "analytics", "statistics", "logs",
                        "welcome", "success", "authenticated", "logged in"
                    ]
                    
                    if any(indicator in response.text.lower() for indicator in auth_bypass_indicators):
                        self.vulnerabilities.append({
                            'type': 'Authentication Bypass',
                            'severity': 'Critical',
                            'url': test_url,
                            'payload': pattern,
                            'parameter': param_name,
                            'description': f'Authentication bypass found in parameter {param_name}'
                        })
                        print(f"[!] Authentication bypass found: {test_url}")
                        
                except Exception as e:
                    continue
                    
        return False
    
    def test_authorization_bypass(self, url):
        """Test for authorization bypasses"""
        print(f"[*] Testing authorization bypasses: {url}")
        
        # Authorization bypass patterns
        authz_bypass_patterns = [
            # Permission manipulation
            "permission=all", "permission=admin", "permission=superuser", "permission=root",
            "permissions=all", "permissions=admin", "permissions=superuser", "permissions=root",
            "access=all", "access=admin", "access=superuser", "access=root",
            "level=admin", "level=superuser", "level=root", "level=0",
            
            # Role escalation
            "role=admin", "role=administrator", "role=superuser", "role=root",
            "user_role=admin", "user_role=administrator", "user_role=superuser",
            "account_type=admin", "account_type=administrator", "account_type=superuser",
            
            # Feature flags
            "feature=all", "feature=admin", "feature=superuser", "feature=root",
            "features=all", "features=admin", "features=superuser", "features=root",
            "enabled=all", "enabled=admin", "enabled=superuser", "enabled=root",
            
            # API access
            "api_access=true", "api_access=1", "api_access=yes", "api_access=on",
            "api_key=admin", "api_key=superuser", "api_key=root", "api_key=all",
            "access_key=admin", "access_key=superuser", "access_key=root", "access_key=all",
        ]
        
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        for param_name, param_values in query_params.items():
            original_value = param_values[0]
            
            for pattern in authz_bypass_patterns:
                try:
                    test_url = url.replace(f"{param_name}={original_value}", f"{param_name}={pattern}")
                    response = self.session.get(test_url, timeout=10)
                    
                    # Check for authorization bypass indicators
                    authz_bypass_indicators = [
                        "admin", "administrator", "superuser", "root",
                        "dashboard", "control panel", "management",
                        "users", "members", "customers", "clients",
                        "orders", "transactions", "payments", "billing",
                        "reports", "analytics", "statistics", "logs",
                        "settings", "configuration", "preferences",
                        "delete", "edit", "modify", "update", "create"
                    ]
                    
                    if any(indicator in response.text.lower() for indicator in authz_bypass_indicators):
                        self.vulnerabilities.append({
                            'type': 'Authorization Bypass',
                            'severity': 'High',
                            'url': test_url,
                            'payload': pattern,
                            'parameter': param_name,
                            'description': f'Authorization bypass found in parameter {param_name}'
                        })
                        print(f"[!] Authorization bypass found: {test_url}")
                        
                except Exception as e:
                    continue
                    
        return False
    
    def discover_business_endpoints(self, base_url):
        """Discover business logic endpoints"""
        print(f"[*] Discovering business endpoints for {base_url}")
        
        # Business logic endpoints
        business_endpoints = [
            # User management
            "/users", "/user", "/profile", "/account", "/settings",
            "/admin/users", "/admin/user", "/admin/profile", "/admin/account",
            "/api/users", "/api/user", "/api/profile", "/api/account",
            
            # Order management
            "/orders", "/order", "/purchases", "/purchase", "/transactions",
            "/admin/orders", "/admin/order", "/admin/purchases", "/admin/purchase",
            "/api/orders", "/api/order", "/api/purchases", "/api/purchase",
            
            # Payment processing
            "/payments", "/payment", "/billing", "/invoice", "/receipt",
            "/admin/payments", "/admin/payment", "/admin/billing", "/admin/invoice",
            "/api/payments", "/api/payment", "/api/billing", "/api/invoice",
            
            # Product management
            "/products", "/product", "/items", "/item", "/catalog",
            "/admin/products", "/admin/product", "/admin/items", "/admin/item",
            "/api/products", "/api/product", "/api/items", "/api/item",
            
            # Content management
            "/content", "/posts", "/post", "/articles", "/article",
            "/admin/content", "/admin/posts", "/admin/post", "/admin/articles",
            "/api/content", "/api/posts", "/api/post", "/api/articles",
            
            # File management
            "/files", "/file", "/uploads", "/upload", "/downloads", "/download",
            "/admin/files", "/admin/file", "/admin/uploads", "/admin/upload",
            "/api/files", "/api/file", "/api/uploads", "/api/upload",
            
            # System management
            "/system", "/config", "/configuration", "/settings", "/preferences",
            "/admin/system", "/admin/config", "/admin/configuration", "/admin/settings",
            "/api/system", "/api/config", "/api/configuration", "/api/settings",
        ]
        
        for endpoint in business_endpoints:
            try:
                full_url = urljoin(base_url, endpoint)
                response = self.session.get(full_url, timeout=5)
                
                if response.status_code == 200:
                    self.endpoints.add(full_url)
                    print(f"[+] Found business endpoint: {full_url}")
                    
            except Exception as e:
                continue
    
    def run_business_logic_scan(self):
        """Run business logic vulnerability scan"""
        print(f"[*] Starting business logic scan for {self.target}")
        
        # Phase 1: Business Endpoint Discovery
        print("\n[1/3] Discovering business endpoints...")
        self.discover_business_endpoints(f"https://{self.target}")
        print(f"[+] Found {len(self.endpoints)} business endpoints")
        
        # Phase 2: Business Logic Testing
        print("\n[2/3] Testing business logic vulnerabilities...")
        for endpoint in list(self.endpoints)[:15]:  # Limit for efficiency
            print(f"[*] Testing business logic: {endpoint}")
            
            # Test all business logic vulnerability types
            self.test_idor_vulnerabilities(endpoint)
            self.test_race_conditions(endpoint)
            self.test_business_logic_bypass(endpoint)
            self.test_authentication_bypass(endpoint)
            self.test_authorization_bypass(endpoint)
        
        # Phase 3: Generate Report
        print("\n[3/3] Generating business logic report...")
        self.generate_business_logic_report()
        
        print(f"\n[+] Business logic scan completed! Found {len(self.vulnerabilities)} vulnerabilities")
        return self.vulnerabilities
    
    def generate_business_logic_report(self):
        """Generate business logic vulnerability report"""
        report_data = {
            "target": self.target,
            "timestamp": datetime.now().isoformat(),
            "endpoints_tested": len(self.endpoints),
            "vulnerabilities_found": len(self.vulnerabilities),
            "vulnerabilities": self.vulnerabilities,
            "summary": {
                "critical": len([v for v in self.vulnerabilities if v['severity'] == 'Critical']),
                "high": len([v for v in self.vulnerabilities if v['severity'] == 'High']),
                "medium": len([v for v in self.vulnerabilities if v['severity'] == 'Medium']),
                "low": len([v for v in self.vulnerabilities if v['severity'] == 'Low'])
            }
        }
        
        # Save report
        os.makedirs("logs/business_logic", exist_ok=True)
        report_filename = f"logs/business_logic/business_logic_scan_{self.target.replace('.', '_')}_{int(time.time())}.json"
        with open(report_filename, 'w') as f:
            json.dump(report_data, f, indent=4)
        print(f"[+] Business logic report saved to: {report_filename}")
        
        # Print summary
        print("\n" + "="*60)
        print("BUSINESS LOGIC VULNERABILITY SCAN SUMMARY")
        print("="*60)
        print(f"Target: {self.target}")
        print(f"Endpoints tested: {len(self.endpoints)}")
        print(f"Vulnerabilities found: {len(self.vulnerabilities)}")
        print(f"Critical: {report_data['summary']['critical']}")
        print(f"High: {report_data['summary']['high']}")
        print(f"Medium: {report_data['summary']['medium']}")
        print(f"Low: {report_data['summary']['low']}")
        print("="*60)
        
        if self.vulnerabilities:
            print("\nBUSINESS LOGIC VULNERABILITIES FOUND:")
            for vuln in self.vulnerabilities:
                print(f"  [{vuln['severity']}] {vuln['type']}: {vuln['url']}")
                print(f"    Parameter: {vuln.get('parameter', 'N/A')}")
                print(f"    Payload: {vuln['payload']}")
                print(f"    Description: {vuln['description']}")
                print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 business_logic_scanner.py <target_domain>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = BusinessLogicScanner(target)
    scanner.run_business_logic_scan()
