#!/usr/bin/env python3
"""
API SECURITY TESTER - REST/GraphQL/WebSocket VULNERABILITY DISCOVERY
Tests for API-specific vulnerabilities and misconfigurations
"""
import requests
import json
import websocket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class APISecurityTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.vulnerabilities = []
        
    def test_all_api_vulnerabilities(self):
        """Test all API security vulnerabilities"""
        print(f"[*] Starting API security testing on {self.target_url}")
        
        self.test_rest_api_vulnerabilities()
        self.test_graphql_vulnerabilities()
        self.test_websocket_vulnerabilities()
        self.test_api_authentication()
        self.test_api_authorization()
        self.test_api_rate_limiting()
        self.test_api_injection()
        
        return self.vulnerabilities
    
    def test_rest_api_vulnerabilities(self):
        """Test REST API vulnerabilities"""
        print("[*] Testing REST API vulnerabilities...")
        
        # Test common API endpoints
        api_endpoints = [
            "/api/v1/users",
            "/api/v1/admin",
            "/api/users",
            "/api/admin",
            "/api/v2/users",
            "/api/v2/admin",
            "/rest/users",
            "/rest/admin"
        ]
        
        for endpoint in api_endpoints:
            try:
                test_url = self.target_url + endpoint
                
                # Test different HTTP methods
                methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
                for method in methods:
                    response = self.session.request(method, test_url, timeout=10)
                    
                    if self._check_api_vulnerability(response, method, endpoint):
                        self.vulnerabilities.append({
                            "type": "REST API Vulnerability",
                            "severity": "High",
                            "url": test_url,
                            "method": method,
                            "status_code": response.status_code
                        })
            except:
                pass
    
    def test_graphql_vulnerabilities(self):
        """Test GraphQL vulnerabilities"""
        print("[*] Testing GraphQL vulnerabilities...")
        
        graphql_endpoints = [
            "/graphql",
            "/api/graphql",
            "/v1/graphql",
            "/query"
        ]
        
        # GraphQL introspection query
        introspection_query = {
            "query": """
            query IntrospectionQuery {
                __schema {
                    queryType { name }
                    mutationType { name }
                    subscriptionType { name }
                    types {
                        ...FullType
                    }
                }
            }
            fragment FullType on __Type {
                kind
                name
                description
                fields(includeDeprecated: true) {
                    name
                    description
                    args {
                        ...InputValue
                    }
                    type {
                        ...TypeRef
                    }
                }
            }
            fragment InputValue on __InputValue {
                name
                description
                type { ...TypeRef }
                defaultValue
            }
            fragment TypeRef on __Type {
                kind
                name
                ofType {
                    kind
                    name
                    ofType {
                        kind
                        name
                    }
                }
            }
            """
        }
        
        for endpoint in graphql_endpoints:
            try:
                test_url = self.target_url + endpoint
                response = self.session.post(test_url, json=introspection_query, timeout=10)
                
                if self._check_graphql_introspection(response):
                    self.vulnerabilities.append({
                        "type": "GraphQL Introspection Enabled",
                        "severity": "Medium",
                        "url": test_url
                    })
                
                # Test GraphQL injection
                injection_queries = [
                    {"query": "query { __typename }"},
                    {"query": "query { user(id: 1) { id name } }"},
                    {"query": "mutation { createUser(input: {name: \"test\"}) { id } }"}
                ]
                
                for query in injection_queries:
                    response = self.session.post(test_url, json=query, timeout=10)
                    if self._check_graphql_injection(response):
                        self.vulnerabilities.append({
                            "type": "GraphQL Injection",
                            "severity": "High",
                            "url": test_url,
                            "query": query
                        })
            except:
                pass
    
    def test_websocket_vulnerabilities(self):
        """Test WebSocket vulnerabilities"""
        print("[*] Testing WebSocket vulnerabilities...")
        
        ws_endpoints = [
            "/ws",
            "/websocket",
            "/api/ws",
            "/socket.io"
        ]
        
        for endpoint in ws_endpoints:
            try:
                ws_url = self.target_url.replace("http", "ws") + endpoint
                
                # Test WebSocket connection
                def test_websocket():
                    try:
                        ws = websocket.create_connection(ws_url, timeout=10)
                        
                        # Send test messages
                        test_messages = [
                            "ping",
                            '{"type": "ping"}',
                            '{"action": "subscribe", "channel": "admin"}',
                            '{"query": "SELECT * FROM users"}'
                        ]
                        
                        for message in test_messages:
                            ws.send(message)
                            result = ws.recv()
                            
                            if self._check_websocket_vulnerability(result, message):
                                self.vulnerabilities.append({
                                    "type": "WebSocket Vulnerability",
                                    "severity": "High",
                                    "url": ws_url,
                                    "message": message
                                })
                        
                        ws.close()
                    except:
                        pass
                
                # Run WebSocket test in thread
                thread = threading.Thread(target=test_websocket)
                thread.start()
                thread.join(timeout=5)
                
            except:
                pass
    
    def test_api_authentication(self):
        """Test API authentication vulnerabilities"""
        print("[*] Testing API authentication...")
        
        # Test API key vulnerabilities
        api_key_headers = [
            "X-API-Key",
            "Authorization",
            "X-Auth-Token",
            "API-Key",
            "X-API-Token"
        ]
        
        test_keys = [
            "test",
            "admin",
            "123456",
            "api_key",
            "secret",
            "key"
        ]
        
        for header in api_key_headers:
            for key in test_keys:
                try:
                    headers = {header: key}
                    response = self.session.get(self.target_url, headers=headers, timeout=10)
                    
                    if self._check_api_auth_bypass(response):
                        self.vulnerabilities.append({
                            "type": "API Authentication Bypass",
                            "severity": "Critical",
                            "url": self.target_url,
                            "header": header,
                            "key": key
                        })
                except:
                    pass
    
    def test_api_authorization(self):
        """Test API authorization vulnerabilities"""
        print("[*] Testing API authorization...")
        
        # Test privilege escalation
        privilege_tests = [
            {"user_id": 1, "admin": True},
            {"role": "admin", "permissions": "all"},
            {"is_admin": True, "user_type": "admin"}
        ]
        
        for test_data in privilege_tests:
            try:
                response = self.session.post(self.target_url, json=test_data, timeout=10)
                
                if self._check_privilege_escalation(response):
                    self.vulnerabilities.append({
                        "type": "API Authorization Bypass",
                        "severity": "Critical",
                        "url": self.target_url,
                        "data": test_data
                    })
            except:
                pass
    
    def test_api_rate_limiting(self):
        """Test API rate limiting"""
        print("[*] Testing API rate limiting...")
        
        # Send multiple requests quickly
        try:
            responses = []
            for i in range(100):
                response = self.session.get(self.target_url, timeout=5)
                responses.append(response.status_code)
            
            if not self._check_rate_limiting(responses):
                self.vulnerabilities.append({
                    "type": "API Rate Limiting Bypass",
                    "severity": "Medium",
                    "url": self.target_url
                })
        except:
            pass
    
    def test_api_injection(self):
        """Test API injection vulnerabilities"""
        print("[*] Testing API injection...")
        
        injection_payloads = [
            {"query": "SELECT * FROM users"},
            {"filter": "1' OR '1'='1"},
            {"search": "<script>alert(1)</script>"},
            {"data": "'; DROP TABLE users; --"}
        ]
        
        for payload in injection_payloads:
            try:
                response = self.session.post(self.target_url, json=payload, timeout=10)
                
                if self._check_injection_vulnerability(response):
                    self.vulnerabilities.append({
                        "type": "API Injection",
                        "severity": "High",
                        "url": self.target_url,
                        "payload": payload
                    })
            except:
                pass
    
    def _check_api_vulnerability(self, response, method, endpoint):
        """Check for API vulnerability indicators"""
        indicators = [
            response.status_code == 200,
            "api" in response.text.lower(),
            "json" in response.headers.get("content-type", ""),
            method in ["PUT", "PATCH", "DELETE"] and response.status_code == 200
        ]
        return sum(indicators) >= 2
    
    def _check_graphql_introspection(self, response):
        """Check for GraphQL introspection"""
        return "schema" in response.text.lower() and response.status_code == 200
    
    def _check_graphql_injection(self, response):
        """Check for GraphQL injection"""
        return response.status_code == 200 and "data" in response.text.lower()
    
    def _check_websocket_vulnerability(self, result, message):
        """Check for WebSocket vulnerability"""
        return len(result) > 0 and "error" not in result.lower()
    
    def _check_api_auth_bypass(self, response):
        """Check for API auth bypass"""
        return response.status_code == 200 and "unauthorized" not in response.text.lower()
    
    def _check_privilege_escalation(self, response):
        """Check for privilege escalation"""
        return response.status_code == 200 and "admin" in response.text.lower()
    
    def _check_rate_limiting(self, responses):
        """Check if rate limiting is working"""
        return any(status == 429 for status in responses)
    
    def _check_injection_vulnerability(self, response):
        """Check for injection vulnerability"""
        return response.status_code == 200 and len(response.text) > 100

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 api_security_tester.py <url>")
        sys.exit(1)
    
    tester = APISecurityTester(sys.argv[1])
    vulns = tester.test_all_api_vulnerabilities()
    
    print(f"\n[+] Found {len(vulns)} potential API vulnerabilities")
    for vuln in vulns:
        print(f"  - {vuln['type']}: {vuln['severity']}")
