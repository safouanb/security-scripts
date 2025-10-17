#!/usr/bin/env python3
"""
SSL Check Example - Demonstrates SSL certificate analysis
Author: Safouan Benali
License: MIT
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.network.ssl_check import parse_and_output
import json

def main():
    """Example usage of SSL checker."""
    print("SSL Certificate Checker Example")
    print("=" * 40)
    
    # Example domains to check
    domains = [
        "github.com",
        "google.com", 
        "stackoverflow.com"
    ]
    
    for domain in domains:
        print(f"\nChecking SSL certificate for: {domain}")
        print("-" * 30)
        
        try:
            # This would normally call the ssl_check function
            # For demo purposes, we'll show the expected output format
            result = {
                "host": domain,
                "valid_chain": True,
                "snippet": "Certificate chain verification successful"
            }
            
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(f"Error checking {domain}: {e}")

if __name__ == "__main__":
    main()
