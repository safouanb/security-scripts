#!/usr/bin/env python3
"""
RACE CONDITION TESTER - TIMING-BASED VULNERABILITY DISCOVERY
Tests for race conditions and timing-based vulnerabilities
"""
import requests
import threading
import time
import json
from concurrent.futures import ThreadPoolExecutor

class RaceConditionTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.vulnerabilities = []
        
    def test_all_race_conditions(self):
        """Test all race condition vulnerabilities"""
        print(f"[*] Starting race condition testing on {self.target_url}")
        
        self.test_purchase_race_condition()
        self.test_account_creation_race()
        self.test_password_reset_race()
        self.test_coupon_race_condition()
        self.test_inventory_race_condition()
        self.test_voting_race_condition()
        
        return self.vulnerabilities
    
    def test_purchase_race_condition(self):
        """Test purchase race condition"""
        print("[*] Testing purchase race condition...")
        
        def make_purchase():
            try:
                data = {
                    "product_id": 1,
                    "quantity": 1,
                    "price": 100
                }
                response = self.session.post(self.target_url, json=data, timeout=10)
                return response
            except:
                return None
        
        # Send multiple purchase requests simultaneously
        threads = []
        responses = []
        
        for i in range(10):
            thread = threading.Thread(target=lambda: responses.append(make_purchase()))
            threads.append(thread)
        
        # Start all threads at the same time
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check for race condition
        if self._check_purchase_race_condition(responses):
            self.vulnerabilities.append({
                "type": "Purchase Race Condition",
                "severity": "High",
                "url": self.target_url,
                "description": "Multiple purchases processed simultaneously"
            })
    
    def test_account_creation_race(self):
        """Test account creation race condition"""
        print("[*] Testing account creation race condition...")
        
        def create_account():
            try:
                data = {
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "password123"
                }
                response = self.session.post(self.target_url, json=data, timeout=10)
                return response
            except:
                return None
        
        # Send multiple account creation requests
        threads = []
        responses = []
        
        for i in range(5):
            thread = threading.Thread(target=lambda: responses.append(create_account()))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        if self._check_account_creation_race(responses):
            self.vulnerabilities.append({
                "type": "Account Creation Race Condition",
                "severity": "Medium",
                "url": self.target_url,
                "description": "Multiple accounts created with same credentials"
            })
    
    def test_password_reset_race(self):
        """Test password reset race condition"""
        print("[*] Testing password reset race condition...")
        
        def request_password_reset():
            try:
                data = {"email": "test@example.com"}
                response = self.session.post(self.target_url, json=data, timeout=10)
                return response
            except:
                return None
        
        # Send multiple password reset requests
        threads = []
        responses = []
        
        for i in range(5):
            thread = threading.Thread(target=lambda: responses.append(request_password_reset()))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        if self._check_password_reset_race(responses):
            self.vulnerabilities.append({
                "type": "Password Reset Race Condition",
                "severity": "High",
                "url": self.target_url,
                "description": "Multiple password reset tokens generated"
            })
    
    def test_coupon_race_condition(self):
        """Test coupon race condition"""
        print("[*] Testing coupon race condition...")
        
        def use_coupon():
            try:
                data = {
                    "coupon_code": "DISCOUNT10",
                    "amount": 100
                }
                response = self.session.post(self.target_url, json=data, timeout=10)
                return response
            except:
                return None
        
        # Send multiple coupon usage requests
        threads = []
        responses = []
        
        for i in range(5):
            thread = threading.Thread(target=lambda: responses.append(use_coupon()))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        if self._check_coupon_race_condition(responses):
            self.vulnerabilities.append({
                "type": "Coupon Race Condition",
                "severity": "High",
                "url": self.target_url,
                "description": "Single coupon used multiple times"
            })
    
    def test_inventory_race_condition(self):
        """Test inventory race condition"""
        print("[*] Testing inventory race condition...")
        
        def update_inventory():
            try:
                data = {
                    "product_id": 1,
                    "quantity": -1
                }
                response = self.session.post(self.target_url, json=data, timeout=10)
                return response
            except:
                return None
        
        # Send multiple inventory update requests
        threads = []
        responses = []
        
        for i in range(10):
            thread = threading.Thread(target=lambda: responses.append(update_inventory()))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        if self._check_inventory_race_condition(responses):
            self.vulnerabilities.append({
                "type": "Inventory Race Condition",
                "severity": "High",
                "url": self.target_url,
                "description": "Inventory count desynchronized"
            })
    
    def test_voting_race_condition(self):
        """Test voting race condition"""
        print("[*] Testing voting race condition...")
        
        def cast_vote():
            try:
                data = {
                    "poll_id": 1,
                    "option": "A"
                }
                response = self.session.post(self.target_url, json=data, timeout=10)
                return response
            except:
                return None
        
        # Send multiple voting requests
        threads = []
        responses = []
        
        for i in range(10):
            thread = threading.Thread(target=lambda: responses.append(cast_vote()))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        if self._check_voting_race_condition(responses):
            self.vulnerabilities.append({
                "type": "Voting Race Condition",
                "severity": "Medium",
                "url": self.target_url,
                "description": "Multiple votes cast by same user"
            })
    
    def _check_purchase_race_condition(self, responses):
        """Check for purchase race condition"""
        success_count = sum(1 for r in responses if r and r.status_code == 200)
        return success_count > 1
    
    def _check_account_creation_race(self, responses):
        """Check for account creation race condition"""
        success_count = sum(1 for r in responses if r and r.status_code == 200)
        return success_count > 1
    
    def _check_password_reset_race(self, responses):
        """Check for password reset race condition"""
        success_count = sum(1 for r in responses if r and r.status_code == 200)
        return success_count > 1
    
    def _check_coupon_race_condition(self, responses):
        """Check for coupon race condition"""
        success_count = sum(1 for r in responses if r and r.status_code == 200)
        return success_count > 1
    
    def _check_inventory_race_condition(self, responses):
        """Check for inventory race condition"""
        success_count = sum(1 for r in responses if r and r.status_code == 200)
        return success_count > 1
    
    def _check_voting_race_condition(self, responses):
        """Check for voting race condition"""
        success_count = sum(1 for r in responses if r and r.status_code == 200)
        return success_count > 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 race_condition_tester.py <url>")
        sys.exit(1)
    
    tester = RaceConditionTester(sys.argv[1])
    vulns = tester.test_all_race_conditions()
    
    print(f"\n[+] Found {len(vulns)} potential race condition vulnerabilities")
    for vuln in vulns:
        print(f"  - {vuln['type']}: {vuln['severity']}")
